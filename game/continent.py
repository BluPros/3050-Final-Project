from dataclasses import dataclass


@dataclass
class Continent:
    name: str
    bonus: int
    territories: list[str]