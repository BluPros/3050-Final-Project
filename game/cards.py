# Defines Risk cards and helper functions for deck creation and card trades.
# Territory symbols are assigned using the order of territories in the map data.

from dataclasses import dataclass, asdict
from itertools import product


SYMBOLS = ("infantry", "cavalry", "artillery")


# Stores the ID, territory, and symbol of a single card.
@dataclass(frozen=True)
class Card:
    """Represents a single Risk card with an ID, territory, and symbol."""
    card_id: str
    territory: str | None
    symbol: str

    # Returns the card information as a dictionary.
    def to_dict(self):
        return asdict(self)


# Creates one card per territory and adds two wild cards.
def make_deck(territories):
    cards = []

    # Alternate between the three symbols in territory insertion order.
    for index, territory_name in enumerate(territories):
        symbol = SYMBOLS[index % len(SYMBOLS)]

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


# Checks whether three different cards form a valid trade set.
def valid_set(cards):
    # A trade must contain exactly three cards.
    if len(cards) != 3:
        return False

    card_ids = {
        card.card_id
        for card in cards
    }

    # The same card cannot appear more than once in a trade.
    if len(card_ids) != 3:
        return False

    allowed_symbols = (*SYMBOLS, "wild")

    if any(card.symbol not in allowed_symbols for card in cards):
        return False

    # Wild cards can represent any of the three regular symbols.
    options = []

    for card in cards:
        if card.symbol == "wild":
            options.append(SYMBOLS)
        else:
            options.append((card.symbol,))

    # A valid set has either three matching symbols or three different
    for values in product(*options):
        symbol_count = len(set(values))

        if symbol_count == 1 or symbol_count == 3:
            return True

    return False

# Calculates the reward based on the number of sets already traded by all players.
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

    # After the sixth trade, each reward increases by five armies.
    return 15 + 5 * (previous_trades - 5)
