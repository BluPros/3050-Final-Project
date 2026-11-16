import argparse
import csv
import random
from contextlib import redirect_stdout
from io import StringIO

import constants
from game.bot_ai import BotAI
from game.game_state import Game
from training.neural_bot import NeuralBot


DIFFICULTIES = ("easy", "medium", "hard")
MAX_ACTIONS = 50000
MAX_ATTACKS_PER_TURN = 30
MAX_TURNS = 500


def create_game(include_neural=False, neural_policy=None):
    """Create and initialize a three-bot Risk match."""
    game = Game()

    # Add neural

    if include_neural:
        difficulties = ("easy", "hard", "neural")
    else:
        difficulties = DIFFICULTIES

    for index, difficulty in enumerate(difficulties):
        game.add_player(
            name=f"{difficulty.capitalize()} Bot",
            color=constants.PLAYER_COLORS[index],
            is_bot=True,
            difficulty=difficulty
        )

    if not game.start_setup():
        raise RuntimeError("Could not initialize the game.")

    bots = {}

    for player in game.players:
        if player.difficulty == "neural":
            from training.neural_bot import NeuralBot
            bots[player.player_id] = NeuralBot(policy=neural_policy)
            print(f"Created Neural bot: {player.name}")
        else:
            bots[player.player_id] = BotAI(difficulty=player.difficulty)

    return game, bots


def perform_action(game, bots, attack_count):
    """Execute one legal bot action and return the attack count."""
    player = game.current_player
    bot = bots[player.player_id]

    if game.phase == "setup_claim":
        available = [
            territory.name
            for territory in game.territories.values()
            if territory.owner_id is None
        ]

        if not available:
            raise RuntimeError("No unclaimed territories.")

        if not game.claim_territory(random.choice(available)):
            raise RuntimeError("Territory claim failed.")

    elif game.phase == "setup_place":
        owned = [
            territory.name
            for territory in game.territories.values()
            if territory.owner_id == player.player_id
        ]

        if not owned:
            raise RuntimeError("Bot has no setup territories.")

        if not game.place_setup_army(random.choice(owned)):
            raise RuntimeError("Setup placement failed.")

    elif game.phase == "deploy":
        if game.must_redeem_cards():
            card_ids = bot.choose_card_trade(game)

            if card_ids is None:
                raise RuntimeError("Required card trade unavailable.")

            game.redeem_card(card_ids)

        elif player.reinforcements > 0:
            action = bot.choose_deployment(game)

            if action is None or not game.deploy(*action):
                raise RuntimeError("Bot deployment failed.")

        else:
            if not game.next_phase():
                raise RuntimeError("Cannot leave deployment.")

            attack_count = 0

    elif game.phase == "attack":
        if game.pending_conquest is not None:
            count = bot.choose_move_in(game)

            if count is None or not game.move_in(count):
                raise RuntimeError("Conquest movement failed.")

        elif attack_count >= MAX_ATTACKS_PER_TURN:
            if not game.next_phase():
                raise RuntimeError("Cannot leave attack phase.")

        else:
            action = bot.choose_attack(game)

            if action is None:
                if not game.next_phase():
                    raise RuntimeError("Cannot leave attack phase.")
            else:
                result = game.attack(*action)

                if result is None:
                    raise RuntimeError(
                        f"Invalid attack by {player.name}: {action}"
                    )

                attack_count += 1

    elif game.phase == "fortify":
        action = bot.choose_fortification(game)

        if action is not None and not game.fortify(*action):
            raise RuntimeError("Bot fortification failed.")

        if not game.next_phase():
            raise RuntimeError("Cannot finish turn.")

    return attack_count


def simulate(game_number, include_neural=False, neural_policy=None):
    """Run a single game until victory or the action limit."""
    game, bots = create_game(include_neural, neural_policy)
    attack_count = 0
    actions = 0
    turns = 0

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

    winner = None

    if game.winner_id is not None:
        winner = game.get_player(game.winner_id)

    if winner is not None:
        stop_reason = "victory"
    elif turns >= MAX_TURNS:
        stop_reason = "turn_limit"
    else:
        stop_reason = "action_limit"

    neural_decisions = sum(
        bot.attack_decisions
        for bot in bots.values()
        if hasattr(bot, "attack_decisions")
    )
    return {
        "game": game_number,
        "winner": winner.name if winner else "No winner",
        "difficulty": winner.difficulty if winner else "",
        "turns": turns,
        "actions": actions,
        "completed": winner is not None,
        "stop_reason": stop_reason,
        "neural_decisions": neural_decisions
    }

# Main function to run multiple games and save their results this is useful for generating heuristic data for developing the
# AI strategies or a custom model
def main():
    """Run multiple games and save their results."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--games", type=int, default=1
    )
    parser.add_argument(
        "--output", default="simulation_results.csv"
    )
    parser.add_argument(
        "--include_neural", action="store_true",
        help="Include a neural network bot in the games."
    )
    args = parser.parse_args()

    if args.games < 1:
        parser.error("--games must be at least 1")

    results = []

    for game_number in range(1, args.games + 1):
        # Suppress normal game-engine debug output.
        with redirect_stdout(StringIO()):
            result = simulate(game_number, include_neural=args.include_neural)

        results.append(result)

        print(
            f"Game {game_number}: "
            f"{result['winner']} | "
            f"{result['turns']} turns | "
            f"{result['actions']} actions"
            f" | Neural decisions: {result['neural_decisions']}"
        )

    with open(
        args.output, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "game", "winner", "difficulty",
                "turns", "actions", "completed", "stop_reason", "neural_decisions"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
