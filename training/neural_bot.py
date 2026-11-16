from game.bot_ai import BotAI
from training.neural_policy import NeuralPolicy


class NeuralBot:
    """Use a neural policy for attacks and Hard AI for other phases."""

    #TODO: Consider using a neural network for all phases, not just attacks.

    def __init__(self, policy=None):
        self.heuristic = BotAI(difficulty="hard")
        self.policy = policy if policy is not None else NeuralPolicy()
        self.attack_decisions = 0

    def choose_deployment(self, game):
        """Use Hard's deployment strategy."""
        return self.heuristic.choose_deployment(game)

    def choose_attack(self, game):
        """Use the neural network to choose an attack."""
        self.attack_decisions += 1
        return self.policy.choose_attack(game)

    def choose_move_in(self, game):
        """Use Hard's conquest-movement strategy."""
        return self.heuristic.choose_move_in(game)

    def choose_fortification(self, game):
        """Use Hard's fortification strategy."""
        return self.heuristic.choose_fortification(game)

    def choose_card_trade(self, game):
        """Use Hard's card-trading strategy."""
        return self.heuristic.choose_card_trade(game)
