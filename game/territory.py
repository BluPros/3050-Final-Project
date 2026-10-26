from dataclasses import dataclass, field


@dataclass
class Territory:
    name: str
    continent: str
    neighbors: list[str]

    # Variable used to identify the territory on the map 
    mask_color: tuple[int, int, int]

    # Variable to identify the position for the label of the territory on the map
    label_position: tuple[int, int]

    owner_id: int | None = None
    troops: int = 0

    # New helper functions to manage territory ownership and troops
    def is_neighbor(self, territory_name: str) -> bool:
        return territory_name in self.neighbors

    def set_owner(self, player_id: int | None):
        self.owner_id = player_id

    def add_troops(self, amount: int):
        self.troops += amount

    def remove_troops(self, amount: int) -> bool:
        if amount > self.troops:
            return False

        self.troops -= amount
        return True