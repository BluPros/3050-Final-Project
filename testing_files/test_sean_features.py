import json
import unittest
from game.game_state import Game
from game.cards import Card, valid_set, trade_value


class SeanTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = self.game.add_player("Sean", (150, 80, 190))
        self.other = self.game.add_player("Other", (0, 0, 255))
        self.game.begin_card_turn()

    def give_set(self):
        cards = self.game.card_deck[:]
        chosen = []
        for symbol in ("infantry", "cavalry", "artillery"):
            chosen.append(next(c for c in cards if c.symbol == symbol))
        for card in chosen:
            self.game.card_deck.remove(card)
        self.player.cards.extend(chosen)
        return [c.card_id for c in chosen]

    def test_deck(self):
        self.assertEqual(len(self.game.card_deck), len(self.game.territories) + 2)
        self.assertEqual(len({c.card_id for c in self.game.card_deck}), len(self.game.card_deck))

    def test_sets(self):
        self.assertTrue(valid_set([Card("a", None, "infantry"), Card("b", None, "cavalry"), Card("c", None, "wild")]))
        self.assertFalse(valid_set([Card("a", None, "infantry"), Card("b", None, "infantry"), Card("c", None, "cavalry")]))

    def test_values(self):
        self.assertEqual([trade_value(i) for i in range(8)], [4, 6, 8, 10, 12, 15, 20, 25])

    def test_trade(self):
        ids = self.give_set()
        self.assertEqual(self.game.redeem_card(ids)["reinforcements"], 4)
        self.assertEqual(self.player.reinforcements, 4)
        self.assertEqual(len(self.game.card_discard), 3)
        self.assertEqual(self.player.cards, [])

    def test_invalid_trade_atomic(self):
        ids = self.give_set()
        before = self.game.state_snapshot()
        with self.assertRaises(ValueError):
            self.game.redeem_card([ids[0], ids[0], ids[1]])
        self.assertEqual(before, self.game.state_snapshot())

    def test_bonus(self):
        ids = self.give_set()
        self.game.assign_territory(ids[0], self.player.player_id, 1)
        self.assertEqual(self.game.redeem_card(ids)["bonus_armies"], 2)
        self.assertEqual(self.game.territories[ids[0]].troops, 3)
        ids = self.give_set()
        self.game.assign_territory(ids[0], self.player.player_id, 1)
        self.assertEqual(self.game.redeem_card(ids)["bonus_armies"], 0)

    def test_reward_once(self):
        self.game.set_card_phase("attack")
        self.game.mark_territory_captured()
        self.game.set_card_phase("end")
        self.assertIsNotNone(self.game.draw_card())
        self.assertIsNone(self.game.draw_card())

    def test_no_capture(self):
        self.game.set_card_phase("end")
        self.assertIsNone(self.game.draw_card())

    def test_wrong_phase(self):
        with self.assertRaises(ValueError):
            self.game.draw_card()
        ids = self.give_set()
        self.game.set_card_phase("attack")
        with self.assertRaises(ValueError):
            self.game.redeem_card(ids)

    def test_mandatory_trade(self):
        self.player.cards.extend(self.game.card_deck[:5])
        del self.game.card_deck[:5]
        with self.assertRaises(ValueError):
            self.game.set_card_phase("attack")

    def test_roll(self):
        rolls = self.game.roll_dice("attacker", 4, 3)
        self.assertEqual(len(rolls), 3)
        self.assertEqual(rolls, sorted(rolls, reverse=True))
        self.assertTrue(all(1 <= n <= 6 for n in rolls))
        with self.assertRaises(ValueError):
            self.game.roll_dice("attacker", 1)

    def test_snapshot_and_display_detached(self):
        self.give_set()
        view = self.game.show_card()
        view[0]["symbol"] = "changed"
        self.assertNotEqual(self.game.show_card()[0]["symbol"], "changed")
        snapshot = self.game.state_snapshot()
        json.dumps(snapshot)
        snapshot["players"][0]["territories"].append("fake")
        self.assertNotIn("fake", self.player.territories)

    def test_transfer(self):
        card = self.game.card_deck.pop()
        self.other.cards.append(card)
        self.assertEqual(self.game.transfer_cards(self.other.player_id), 1)
        self.assertIn(card, self.player.cards)
        self.assertEqual(self.other.cards, [])

    def test_recycle(self):
        ids = self.give_set()
        self.game.redeem_card(ids)
        self.other.cards.extend(self.game.card_deck)
        self.game.card_deck.clear()
        self.game.set_card_phase("attack")
        self.game.mark_territory_captured()
        self.game.set_card_phase("end")
        self.assertIsNotNone(self.game.draw_card())
        self.assertEqual(len(self.game.card_deck), 2)

if __name__ == "__main__":
    unittest.main()
