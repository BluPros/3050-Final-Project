"""Risk cards: no pygame dependency. Territory symbols follow map insertion order."""
from dataclasses import dataclass, asdict
from itertools import product

SYMBOLS = ("infantry", "cavalry", "artillery")

@dataclass(frozen=True)
class Card:
    card_id: str
    territory: str | None
    symbol: str

    def to_dict(self):
        return asdict(self)


def make_deck(territories):
    cards = [Card(name, name, SYMBOLS[i % 3]) for i, name in enumerate(territories)]
    return cards + [Card("wild-1", None, "wild"), Card("wild-2", None, "wild")]


def valid_set(cards):
    if len(cards) != 3 or len({c.card_id for c in cards}) != 3:
        return False
    if any(c.symbol not in (*SYMBOLS, "wild") for c in cards):
        return False
    options = [SYMBOLS if c.symbol == "wild" else (c.symbol,) for c in cards]
    return any(len(set(values)) in (1, 3) for values in product(*options))


def trade_value(previous_trades):
    if type(previous_trades) is not int or previous_trades < 0:
        raise ValueError("Trade count must be a nonnegative integer.")
    return (4, 6, 8, 10, 12, 15)[previous_trades] if previous_trades < 6 else 15 + 5 * (previous_trades - 5)
