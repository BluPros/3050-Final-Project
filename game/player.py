from dataclasses import dataclass, field
import pygame
import constants


@dataclass
class Player:
    player_id: int
    name: str
    color: tuple[int, int, int]

    territories: list[str] = field(default_factory=list)
    reinforcements: int = 0
    
    is_bot: bool = False
    eliminated: bool = False

    # Details for drawing player cards on playing screen
    x_center = 0
    y_center = constants.CARD_Y_CENTER

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

    def draw(self, surface):
        # Draw Background Rectangle
        bg_rect = pygame.Rect(self.x_center - constants.CARD_WIDTH // 2, self.y_center - constants.CARD_HEIGHT // 2,
                              constants.CARD_WIDTH, constants.CARD_HEIGHT)
        pygame.draw.rect(surface, self.color, bg_rect)
        # Write the player info to the screen
        font = pygame.font.SysFont(constants.FONT_STYLE, 14)
        text_surface = font.render(f"{self.name}\n"
                                   f"Troop Count: {self.reinforcements}\n"
                                   f"Terr. Count: {len(self.territories)}",
                                   True,
                                   constants.TEXT_COLOR)
        text_x = self.x_center
        text_y = self.y_center - constants.CARD_HEIGHT // 4
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)