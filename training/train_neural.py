import argparse
import csv
import os
import random
from contextlib import redirect_stdout
from io import StringIO

import tensorflow as tf

from simulation import (
    MAX_ACTIONS,
    MAX_TURNS,
    create_game,
    perform_action,
)

from training.neural_policy import NeuralPolicy


def play_game(policy, max_decisions=48, train=True):
    """Play one game with the shared neural policy."""
    game, bots = create_game(include_neural=True)

    neural_player = next(
        player
        for player in game.players
        if player.difficulty == "neural"
    )

    neural_bot = bots[neural_player.player_id]

    # Reuse the same model instead of creating a new one.
    neural_bot.policy = policy

    policy.trajectory = []
    policy.training = train

    turns = 0
    actions = 0
    attack_count = 0

    try:
        with redirect_stdout(StringIO()):
            while (
                game.phase != "game_over"
                and turns < MAX_TURNS
                and actions < MAX_ACTIONS
            ):
                previous_phase = game.phase

                attack_count = perform_action(
                    game, bots, attack_count
                )

                actions += 1

                if previous_phase == "fortify":
                    turns += 1
    finally:
        policy.training = False

    # Calculate reward to give the neural network based on the game outcome.
    if game.winner_id == neural_player.player_id:
        reward = 1.0
        outcome = "win"
    elif game.winner_id is None:
        reward = 0.0
        outcome = "draw"
    else:
        reward = -1.0
        outcome = "loss"

    trajectory = policy.trajectory

    # Limit the number of decisions per game used in training to avoid memory issues.
    if len(trajectory) > max_decisions:
        trajectory = random.sample(
            trajectory, max_decisions
        )

    policy.trajectory = []

    return {
        "trajectory": trajectory,
        "reward": reward,
        "outcome": outcome,
        "turns": turns,
        "actions": actions,
        "neural_decisions": neural_bot.attack_decisions,
    }


def update_policy(policy, games):
    """Update the weights for the model."""
    usable = [
        game
        for game in games
        if game["trajectory"] and game["reward"] != 0
    ]

    if not usable:
        return None

    with tf.GradientTape() as tape:
        game_losses = []

        for game in usable:
            log_probabilities = []

            for features, chosen_index in game["trajectory"]:
                inputs = tf.convert_to_tensor(
                    features,
                    dtype=tf.float32
                )

                logits = tf.squeeze(
                    policy.model(inputs, training=True),
                    axis=-1
                )

                log_probs = tf.nn.log_softmax(logits)

                log_probabilities.append(
                    log_probs[chosen_index]
                )

            mean_log_prob = tf.reduce_mean(
                tf.stack(log_probabilities)
            )

            game_losses.append(
                -game["reward"] * mean_log_prob
            )

        loss = tf.reduce_mean(
            tf.stack(game_losses)
        )

    gradients = tape.gradient(
        loss,
        policy.model.trainable_variables
    )

    gradient_pairs = [
        (gradient, variable)
        for gradient, variable in zip(
            gradients,
            policy.model.trainable_variables
        )
        if gradient is not None
    ]

    if gradient_pairs:
        clipped, _ = tf.clip_by_global_norm(
            [gradient for gradient, _ in gradient_pairs],
            1.0
        )

        policy.optimizer.apply_gradients(
            zip(
                clipped,
                [
                    variable
                    for _, variable in gradient_pairs
                ]
            )
        )

    return float(loss.numpy())


def main():
    """Train, save the model, and evaluate its performance."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--games", type=int, default=4
    )
    parser.add_argument(
        "--batch-size", type=int, default=4
    )
    parser.add_argument(
        "--evaluate", type=int, default=0
    )
    parser.add_argument(
        "--max-decisions", type=int, default=48
    )
    parser.add_argument(
        "--checkpoint",
        default="training/checkpoints/neural.weights.h5"
    )
    parser.add_argument(
        "--output",
        default="training/training_results.csv"
    )
    parser.add_argument(
        "--resume", action="store_true"
    )
    parser.add_argument(
        "--seed", type=int, default=42
    )

    args = parser.parse_args()

    # Validate arguments
    if args.games < 0:
        parser.error("--games cannot be negative")

    if args.batch_size < 1 or args.max_decisions < 1:
        parser.error("Batch size and decision cap must be positive")

    if args.games == 0 and args.evaluate < 1:
        parser.error("Specify training or evaluation games")

    random.seed(args.seed)
    tf.random.set_seed(args.seed)

    # This policy stays alive across every training game.
    policy = NeuralPolicy()

    # Resume from checkpoint if requested.
    if args.resume:
        if not os.path.isfile(args.checkpoint):
            parser.error(
                f"Missing checkpoint: {args.checkpoint}"
            )

        policy.model.load_weights(args.checkpoint)

        print(
            f"Resumed weights from {args.checkpoint}"
        )

    # Create directories for checkpoint and output files if they don't exist.
    os.makedirs(
        os.path.dirname(
            os.path.abspath(args.checkpoint)
        ),
        exist_ok=True
    )

    os.makedirs(
        os.path.dirname(
            os.path.abspath(args.output)
        ),
        exist_ok=True
    )

    results = []
    batch = []

    # Training games are played first, then evaluation games.
    for game_number in range(1, args.games + 1):
        game = play_game(
            policy,
            args.max_decisions,
            train=True
        )

        batch.append(game)

        results.append({
            "game": game_number,
            "mode": "training",
            "outcome": game["outcome"],
            "turns": game["turns"],
            "actions": game["actions"],
            "neural_decisions": game["neural_decisions"],
        })

        print(
            f"Train {game_number}/{args.games}: "
            f"{game['outcome']} | "
            f"{game['turns']} turns | "
            f"{game['neural_decisions']} neural decisions",
            flush=True
        )

        # Train after each batch.
        if (
            len(batch) == args.batch_size
            or game_number == args.games
        ):
            loss = update_policy(policy, batch)

            policy.model.save_weights(
                args.checkpoint
            )

            print(
                f"  Update: loss={loss} | "
                f"checkpoint={args.checkpoint}",
                flush=True
            )

            batch.clear()

    # Evaluation does not update weights.
    for test_number in range(1, args.evaluate + 1):
        game = play_game(
            policy,
            args.max_decisions,
            train=False
        )

        results.append({
            "game": test_number,
            "mode": "evaluation",
            "outcome": game["outcome"],
            "turns": game["turns"],
            "actions": game["actions"],
            "neural_decisions": game["neural_decisions"],
        })

        print(
            f"Evaluate {test_number}/{args.evaluate}: "
            f"{game['outcome']} | "
            f"{game['neural_decisions']} neural decisions",
            flush=True
        )

    with open(
        args.output,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "game",
                "mode",
                "outcome",
                "turns",
                "actions",
                "neural_decisions",
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(
        f"Results saved to {args.output}"
    )


if __name__ == "__main__":
    main()
