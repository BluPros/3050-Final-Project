
import tensorflow as tf

from training.observations import (
    OBSERVATION_SIZE,
    ACTION_SIZE,
    encode_state_action,
    legal_attack_actions
)

INPUT_SIZE = OBSERVATION_SIZE + ACTION_SIZE


def create_model():
    """Create a neural network that scores possible attacks."""
    return tf.keras.Sequential([
        tf.keras.Input(shape=(INPUT_SIZE,)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(1)
    ])


class NeuralPolicy:
    """Use the neural network to score legal Risk attacks."""

    def __init__(self):
        self.model = create_model()

        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=0.0001
        )
        self.training = False
        self.trajectory = []

    def action_scores(self, game):
        """Return legal attacks and their network scores."""
        actions = legal_attack_actions(game)

        if not actions:
            return [], None

        features = [
            encode_state_action(game, action)
            for action in actions
        ]

        inputs = tf.convert_to_tensor(
            features,
            dtype=tf.float32
        )

        scores = self.model(inputs, training=False)

        return actions, tf.squeeze(scores, axis=-1)

    def choose_attack(self, game):
        """Choose the highest-scoring legal attack."""
        actions = legal_attack_actions(game)

        if not actions:
            return None

        features = [
            encode_state_action(game, action)
            for action in actions
        ]

        inputs = tf.convert_to_tensor(features, dtype=tf.float32)
        scores = tf.squeeze(self.model(inputs, training=False), axis=-1)

        # Defines a training and evaluation mode
        # crucial for the reinforcement learning training loop
        if self.training:
            # randomly choose an action based on the scores for exploration
            choice = int(tf.random.categorical(scores[None, :], 1)[0, 0])
            # save decision to update the training
            self.trajectory.append((features, choice))
        else:
            # When testing pick the action with the highest score.
            choice = int(tf.argmax(scores))

        return actions[choice]