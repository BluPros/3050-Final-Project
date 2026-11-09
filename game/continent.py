from dataclasses import dataclass


@dataclass
class Continent:
    """Represents a continent in the game of Risk with a name, bonus, and list of territories."""
    name: str
    bonus: int
    territories: list[str]
