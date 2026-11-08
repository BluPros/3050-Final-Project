import random
from typing import Literal


class RiskDice:
    def __init__(self, role: Literal["attacker", "defender"]):
        if role not in ("attacker", "defender"):
            raise ValueError("Role must be 'attacker' or 'defender'.")

        self.role = role

    def max_dice(self, armies: int) -> int:
        """Return the maximum legal dice count for this army count."""
        if type(armies) is not int or armies < 1:
            raise ValueError("Armies must be a positive integer.")

        if self.role == "attacker":
            return min(3, armies - 1)

        return min(2, armies)

    def roll(self, armies: int, num_dice: int | None = None) -> list[int]:
        """
        Roll the requested number of dice.

        armies: Total armies in this player's involved territory.
        num_dice: Dice to roll; defaults to the maximum allowed.
        Returns: Dice values sorted from highest to lowest.
        """
        maximum = self.max_dice(armies)

        if maximum == 0:
            raise ValueError("Attacking requires at least 2 armies.")

        if num_dice is None:
            num_dice = maximum

        if type(num_dice) is not int or not 1 <= num_dice <= maximum:
            raise ValueError(
                f"With {armies} armies, the {self.role} must roll "
                f"between 1 and {maximum} dice."
            )

        return sorted(
            [random.randint(1, 6) for _ in range(num_dice)],
            reverse=True,
        )

# compares two ordered lists of RiskDice.roll() sorted high to
# low, returns dead_attackers, dead_defenders
def compare_rolls(attacker, defender):
    dead_attackers = 0
    dead_defenders = 0
    # zip will stop at shortest list, so auto removes lowest roll
    for a_roll, d_roll in zip(attacker, defender):
        if a_roll > d_roll:
            dead_defenders += 1
        else:
            dead_attackers += 1

    return dead_attackers, dead_defenders