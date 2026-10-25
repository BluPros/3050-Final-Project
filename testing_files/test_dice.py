"""Tests for dice.py. Run with: python -m unittest -v test_dice.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from unittest.mock import call, patch

from game.dice import RiskDice


class TestRiskDice(unittest.TestCase):
    def test_valid_roles(self):
        for role in ("attacker", "defender"):
            with self.subTest(role=role):
                self.assertEqual(RiskDice(role).role, role)

    def test_invalid_roles(self):
        for role in ("", "Attacker", "DEFENDER", "spectator", None, 1, [], {}):
            with self.subTest(role=role):
                with self.assertRaises(ValueError):
                    RiskDice(role)

    def test_attacker_max_dice(self):
        for armies, expected in ((1, 0), (2, 1), (3, 2), (4, 3), (5, 3), (100, 3)):
            with self.subTest(armies=armies):
                self.assertEqual(RiskDice("attacker").max_dice(armies), expected)

    def test_defender_max_dice(self):
        for armies, expected in ((1, 1), (2, 2), (3, 2), (100, 2)):
            with self.subTest(armies=armies):
                self.assertEqual(RiskDice("defender").max_dice(armies), expected)

    def test_invalid_armies(self):
        for role in ("attacker", "defender"):
            dice = RiskDice(role)
            for armies in (0, -1, -100, 1.0, 2.5, "3", None, True, False, [], {}):
                for method in (dice.max_dice, dice.roll):
                    with self.subTest(role=role, armies=armies, method=method.__name__):
                        with self.assertRaises(ValueError):
                            method(armies)

    def test_attacker_cannot_roll_with_one_army(self):
        for count in (None, 0, 1):
            with self.subTest(count=count):
                with self.assertRaisesRegex(ValueError, "at least 2 armies"):
                    RiskDice("attacker").roll(1, count)

    def test_default_roll_uses_maximum(self):
        cases = (("attacker", 2, 1), ("attacker", 3, 2), ("attacker", 4, 3),
                 ("attacker", 100, 3), ("defender", 1, 1), ("defender", 2, 2),
                 ("defender", 100, 2))
        for role, armies, expected in cases:
            with self.subTest(role=role, armies=armies):
                with patch("game.dice.random.randint", return_value=4) as randint:
                    self.assertEqual(RiskDice(role).roll(armies), [4] * expected)
                    self.assertEqual(randint.call_args_list, [call(1, 6)] * expected)

    def test_explicit_none_uses_maximum(self):
        with patch("game.dice.random.randint", return_value=6) as randint:
            self.assertEqual(RiskDice("attacker").roll(4, None), [6, 6, 6])
            self.assertEqual(randint.call_count, 3)

    def test_all_legal_explicit_counts(self):
        for role, armies, maximum in (("attacker", 2, 1), ("attacker", 3, 2),
                                     ("attacker", 4, 3), ("defender", 1, 1),
                                     ("defender", 2, 2)):
            for count in range(1, maximum + 1):
                with self.subTest(role=role, armies=armies, count=count):
                    with patch("game.dice.random.randint", return_value=2) as randint:
                        self.assertEqual(RiskDice(role).roll(armies, count), [2] * count)
                        self.assertEqual(randint.call_args_list, [call(1, 6)] * count)

    def test_invalid_dice_counts(self):
        cases = (("attacker", 2, 1), ("attacker", 3, 2), ("attacker", 4, 3),
                 ("defender", 1, 1), ("defender", 2, 2))
        for role, armies, maximum in cases:
            for count in (0, -1, maximum + 1, 100, 1.0, "1", True, False, [], {}):
                with self.subTest(role=role, armies=armies, count=count):
                    with patch("game.dice.random.randint") as randint:
                        with self.assertRaises(ValueError):
                            RiskDice(role).roll(armies, count)
                        randint.assert_not_called()

    def test_roll_sorted_descending(self):
        with patch("game.dice.random.randint", side_effect=[1, 6, 3]):
            self.assertEqual(RiskDice("attacker").roll(4), [6, 3, 1])

    def test_roll_preserves_duplicate_values(self):
        with patch("game.dice.random.randint", side_effect=[2, 5, 5]):
            self.assertEqual(RiskDice("attacker").roll(4), [5, 5, 2])

    def test_defender_roll_sorted_descending(self):
        with patch("game.dice.random.randint", side_effect=[1, 6]):
            self.assertEqual(RiskDice("defender").roll(2), [6, 1])


if __name__ == "__main__":
    unittest.main()
