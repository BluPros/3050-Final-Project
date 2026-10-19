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

    def is_neighbor(self, territory_name: str) -> bool:
        return territory_name in self.neighbors