from dataclasses import dataclass, field


@dataclass
class Player:
    player_id: int
    name: str
    color: tuple[int, int, int]

    territories: list[str] = field(default_factory=list)
    reinforcements: int = 0

    # Helper functions to manage territories and reinforcements
    def add_territory(self, territory_name: str):
        if territory_name not in self.territories:
            self.territories.append(territory_name)

    def remove_territory(self, territory_name: str):
        if territory_name in self.territories:
            self.territories.remove(territory_name)

    def owns_territory(self, territory_name: str) -> bool:
        return territory_name in self.territories

    def territory_count(self) -> int:
        return len(self.territories)

    def add_reinforcements(self, amount: int):
        self.reinforcements += amount

    def use_reinforcements(self, amount: int) -> bool:
        if amount > self.reinforcements:
            return False

        self.reinforcements -= amount
        return True