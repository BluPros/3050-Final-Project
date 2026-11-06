"""Card and dice API for Game. Turn/battle orchestration stays with the game loop."""
import random
from game.cards import make_deck, valid_set, trade_value
from game.dice import RiskDice


class SeanFeatures:
    def _init_sean_features(self):
        self.card_deck = make_deck(self.territories)
        random.shuffle(self.card_deck)
        self.card_discard = []
        self.card_trades = 0
        self.card_phase = "setup"
        self._card_turn_player = None
        self._captured_this_turn = False
        self._card_drawn_this_turn = False
        self._territory_bonus_used = False

    def _card_player(self, player_id=None):
        player = self.current_player if player_id is None else self.get_player(player_id)
        if player is None:
            raise ValueError("Unknown player or no current player.")
        return player

    def _require_card_turn(self):
        player = self._card_player()
        if player.player_id != self._card_turn_player:
            raise ValueError("Call begin_card_turn for the current player first.")
        return player

    def begin_card_turn(self):
        """Call ONCE after the loop selects the next current player."""
        player = self._card_player()
        self._card_turn_player = player.player_id
        self.card_phase = "deploy"
        self._captured_this_turn = False
        self._card_drawn_this_turn = False
        self._territory_bonus_used = False

    def set_card_phase(self, phase):
        """Mirror the loop's phase. This does not implement turn progression."""
        self._require_card_turn()
        if phase not in ("deploy", "attack", "fortify", "end"):
            raise ValueError("Unknown card phase.")
        if phase != "deploy" and self.must_redeem_cards():
            raise ValueError("Trade cards before leaving deployment.")
        self.card_phase = phase

    def mark_territory_captured(self):
        """Battle code calls this only AFTER a successful enemy conquest."""
        self._require_card_turn()
        if self.card_phase != "attack":
            raise ValueError("Captures must occur in the attack phase.")
        self._captured_this_turn = True

    def draw_card(self):
        """End-of-turn reward; None when no capture, already drawn, or deck exhausted."""
        player = self._require_card_turn()
        if self.card_phase != "end":
            raise ValueError("Reward cards are drawn at the end of a turn.")
        if not self._captured_this_turn or self._card_drawn_this_turn:
            return None
        if not self.card_deck and self.card_discard:
            self.card_deck = self.card_discard[:]
            self.card_discard.clear()
            random.shuffle(self.card_deck)
        if not self.card_deck:
            return None
        card = self.card_deck.pop()
        player.cards.append(card)
        self._card_drawn_this_turn = True
        return card

    def show_card(self, player_id=None):
        """Return detached dictionaries for UI rendering; does not draw pygame widgets."""
        return [card.to_dict() for card in self._card_player(player_id).cards]

    def must_redeem_cards(self):
        return len(self._card_player().cards) >= 5

    def redeem_card(self, card_ids, bonus_territory=None):
        """Trade exactly three IDs; award pool armies and optional +2 on one owned card territory."""
        player = self._require_card_turn()
        if self.card_phase != "deploy":
            raise ValueError("Trade cards during deployment.")
        ids = list(card_ids)
        if len(ids) != 3 or len(set(ids)) != 3:
            raise ValueError("Select three distinct card IDs.")
        hand = {card.card_id: card for card in player.cards}
        if any(card_id not in hand for card_id in ids):
            raise ValueError("Selected card is not in your hand.")
        selected = [hand[card_id] for card_id in ids]
        if not valid_set(selected):
            raise ValueError("Not a valid Risk card set.")
        eligible = [c.territory for c in selected if c.territory in self.territories
                    and self.territories[c.territory].owner_id == player.player_id]
        if bonus_territory is not None and (self._territory_bonus_used or bonus_territory not in eligible):
            raise ValueError("Territory bonus unavailable for that territory.")
        bonus = None if self._territory_bonus_used else (bonus_territory or next(iter(eligible), None))
        armies = trade_value(self.card_trades)
        player.cards[:] = [c for c in player.cards if c.card_id not in ids]
        self.card_discard.extend(selected)
        self.card_trades += 1
        player.add_reinforcements(armies)
        if bonus is not None:
            self.territories[bonus].add_troops(2)
            self._territory_bonus_used = True
        return {"reinforcements": armies, "bonus_territory": bonus, "bonus_armies": 2 if bonus else 0}

    def roll_dice(self, role, armies, num_dice=None):
        """Reuse existing legal-dice validation. No casualties or ownership mutations."""
        return RiskDice(role).roll(armies, num_dice)

    def transfer_cards(self, eliminated_player_id):
        """Battle code calls after elimination. Special mid-attack trading is not implemented."""
        winner = self._require_card_turn()
        loser = self._card_player(eliminated_player_id)
        if winner is loser or any(t.owner_id == loser.player_id for t in self.territories.values()):
            raise ValueError("Player is not an eliminated opponent.")
        count = len(loser.cards)
        winner.cards.extend(loser.cards)
        loser.cards.clear()
        return count

    def state_snapshot(self):
        """Detached JSON-compatible state for debugging/future trusted-server integration.

        FULL snapshot includes all hands/deck: never broadcast it to opponents.
        Not a network protocol, save loader, or random-generator checkpoint.
        """
        return {
            "schema_version": 1,
            "current_player_index": self.current_player_index,
            "players": [{"player_id": p.player_id, "name": p.name, "color": list(p.color),
                         "territories": list(p.territories), "reinforcements": p.reinforcements,
                         "cards": [c.to_dict() for c in p.cards]} for p in self.players],
            "territories": {name: {"owner_id": t.owner_id, "troops": t.troops}
                            for name, t in self.territories.items()},
            "cards": {"deck": [c.to_dict() for c in self.card_deck],
                      "discard": [c.to_dict() for c in self.card_discard],
                      "trades": self.card_trades, "phase": self.card_phase,
                      "turn_player": self._card_turn_player,
                      "captured": self._captured_this_turn, "drawn": self._card_drawn_this_turn,
                      "territory_bonus_used": self._territory_bonus_used}}
