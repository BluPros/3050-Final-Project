"""Territory dataclass holds helper functions to manage troops and ownership."""
from dataclasses import dataclass

@dataclass
class Territory:
    """
    Class representing individual territories, each territory is apart of a continent,
     has defined neighbors per the adj. list, keeps track of drawing values(position/color),
     and holds value owner and number of troops.
    """

    name: str
    continent: str
    neighbors: list[str]

    # Variable used to identify the territory on the map
    mask_color: tuple[int, int, int]

    # Variable to identify the position for the label of the territory on the map
    label_position: tuple[int, int]

    owner_id: int | None = None
    troops: int = 0

    def is_neighbor(self, territory_name: str) -> bool:
        """Checks if given string is in set of neighbors, 
           returns True if found, otherwise False"""
        return territory_name in self.neighbors

    def set_owner(self, player_id: int | None):
        """Changes current territory owner_id"""
        self.owner_id = player_id

    def add_troops(self, amount: int):
        """Adds troops stored locally by amount"""
        self.troops += amount

    def remove_troops(self, amount: int) -> bool:
        """Removes amount troops from troops"""
        if amount > self.troops:
            return False

        self.troops -= amount
        return True

        