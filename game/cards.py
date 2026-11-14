# Defines Risk cards and helpers for decks, hands, and trades
# Territory symbols match the symbols on the card images

from dataclasses import dataclass, asdict
from itertools import combinations, product
import random


SYMBOLS = ("infantry", "cavalry", "artillery")

TERRITORY_SYMBOLS = {
    "Afghanistan": "infantry",
    "Alaska": "infantry",
    "Alberta": "infantry",
    "Argentina": "infantry",
    "Brazil": "infantry",
    "Central America": "cavalry",
    "China": "artillery",
    "Congo": "artillery",
    "East Africa": "infantry",
    "Eastern Australia": "cavalry",
    "Eastern United States": "cavalry",
    "Egypt": "cavalry",
    "Great Britain": "infantry",
    "Greenland": "artillery",
    "Iceland": "cavalry",
    "India": "cavalry",
    "Indonesia": "infantry",
    "Irkutsk": "artillery",
    "Japan": "cavalry",
    "Kamchatka": "artillery",
    "Madagascar": "cavalry",
    "Middle East": "artillery",
    "Mongolia": "cavalry",
    "New Guinea": "cavalry",
    "North Africa": "cavalry",
    "Northern Europe": "cavalry",
    "Northwest Territory": "infantry",
    "Ontario": "cavalry",
    "Peru": "cavalry",
    "Quebec": "artillery",
    "Scandinavia": "infantry",
    "Siam": "cavalry",
    "Siberia": "infantry",
    "South Africa": "artillery",
    "Southern Europe": "infantry",
    "Ukraine": "infantry",
    "Ural": "infantry",
    "Venezuela": "cavalry",
    "Western Australia": "artillery",
    "Western Europe": "infantry",
    "Western United States": "cavalry",
    "Yakutsk": "artillery",
}

# Stores the ID, territory, and symbol of a card
@dataclass(frozen=True)
class Card:
    """Represents a single Risk card"""
    card_id: str
    territory: str | None
    symbol: str

    # Returns the card as a dictionary
    def to_dict(self):
        return asdict(self)


# Creates one card per territory and two wild cards
def make_deck(territories):
    cards = []

    # Use the symbol shown on each card image
    for territory_name in territories:
        symbol = TERRITORY_SYMBOLS[territory_name]

        card = Card(
            card_id=territory_name,
            territory=territory_name,
            symbol=symbol
        )

        cards.append(card)

    cards.append(
        Card(
            card_id="wild-1",
            territory=None,
            symbol="wild"
        )
    )

    cards.append(
        Card(
            card_id="wild-2",
            territory=None,
            symbol="wild"
        )
    )

    return cards

# Shuffles the deck in place
def shuffle_deck(deck, rng=None):
    if rng is None:
        rng = random

    rng.shuffle(deck)
    return deck


# Draws the last card and refills from discards if needed
def draw_card(deck, discard_pile=None, rng=None):
    if not deck and discard_pile:
        deck.extend(discard_pile)
        discard_pile.clear()
        shuffle_deck(deck, rng)

    if not deck:
        return None

    return deck.pop()


# Checks whether three different cards form a valid set
def valid_set(cards):
    if len(cards) != 3:
        return False

    card_ids = {
        card.card_id
        for card in cards
    }

    # Reject repeated cards
    if len(card_ids) != 3:
        return False

    allowed_symbols = (*SYMBOLS, "wild")

    if any(card.symbol not in allowed_symbols for card in cards):
        return False

    # Wild cards can use any regular symbol
    options = []

    for card in cards:
        if card.symbol == "wild":
            options.append(SYMBOLS)
        else:
            options.append((card.symbol,))

    # Accept matching symbols or three different symbols
    for values in product(*options):
        symbol_count = len(set(values))

        if symbol_count == 1 or symbol_count == 3:
            return True

    return False


# Finds every valid three-card set in a hand
def find_valid_sets(hand):
    return [
        list(cards)
        for cards in combinations(hand, 3)
        if valid_set(cards)
    ]


# Checks whether a hand has a valid set
def has_valid_set(hand):
    return any(
        valid_set(cards)
        for cards in combinations(hand, 3)
    )


# Calculates the reward using the global trade count
def trade_value(previous_trades):
    if (
        not isinstance(previous_trades, int)
        or isinstance(previous_trades, bool)
        or previous_trades < 0
    ):
        raise ValueError("Trade count must be a nonnegative integer.")

    starting_values = (4, 6, 8, 10, 12, 15)

    if previous_trades < len(starting_values):
        return starting_values[previous_trades]

    # Increase rewards by five after the sixth trade
    return 15 + 5 * (previous_trades - 5)


# Removes a valid set from the hand and returns its reward
def redeem_cards(hand, selected_cards, previous_trades, discard_pile):
    selected_cards = list(selected_cards)

    # Reject invalid trades before changing any lists
    if not valid_set(selected_cards):
        raise ValueError("Select three cards that form a valid set.")

    if hand is discard_pile:
        raise ValueError("The hand and discard pile must be different lists.")

    remaining_cards = list(hand)

    for card in selected_cards:
        if card not in remaining_cards:
            raise ValueError("Every selected card must belong to the player.")

        remaining_cards.remove(card)

    reward = trade_value(previous_trades)

    hand[:] = remaining_cards
    discard_pile.extend(selected_cards)

    return reward
