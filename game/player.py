# Defines each player's information, territories, reinforcements, and cards.
# Also draws the player's information panel on the playing screen.

from dataclasses import dataclass, field

import pygame
import constants


@dataclass
class Player:
    """Stores information about a player, including their territories, reinforcements, and cards."""
    player_id: int
    name: str
    color: tuple[int, int, int]

    territories: list[str] = field(default_factory=list)
    reinforcements: int = 0
    cards: list = field(default_factory=list)

    is_bot: bool = False
    eliminated: bool = False

    # Details for drawing player information panels on the playing screen.
    x_center = 0
    y_center = constants.CARD_Y_CENTER

    # Adds a territory to the player's ownership list.
    def add_territory(self, territory_name: str):
        if territory_name not in self.territories:
            self.territories.append(territory_name)

    # Removes a territory from the player's ownership list.
    def remove_territory(self, territory_name: str):
        if territory_name in self.territories:
            self.territories.remove(territory_name)

    # Checks whether the player owns the requested territory.
    def owns_territory(self, territory_name: str) -> bool:
        return territory_name in self.territories

    # Returns the number of territories owned by the player.
    def territory_count(self) -> int:
        return len(self.territories)

    # Adds armies to the player's available reinforcement supply.
    def add_reinforcements(self, amount: int):
        self.reinforcements += amount

    # Uses reinforcements if the player has enough available.
    def use_reinforcements(self, amount: int) -> bool:
        if amount > self.reinforcements:
            return False

        self.reinforcements -= amount

        return True

    # Draws the player's information panel on the playing screen.
    def draw(self, surface):
        # Draw the background rectangle.
        bg_rect = pygame.Rect(
            self.x_center - constants.CARD_WIDTH // 2,
            self.y_center - constants.CARD_HEIGHT // 2,
            constants.CARD_WIDTH,
            constants.CARD_HEIGHT
        )

        pygame.draw.rect(surface, self.color, bg_rect)

        # Create the font and player information text.
        font = pygame.font.SysFont(
            constants.FONT_STYLE,
            14
        )

        lines = [
            self.name,
            f"Troop Count: {self.reinforcements}",
            f"Terr. Count: {len(self.territories)}"
        ]

        y = self.y_center - constants.CARD_HEIGHT // 2 + constants.CARD_TEXT_PADDING
        for line in lines:
            surf = font.render(line, True, constants.TEXT_COLOR)
            surface.blit(surf, surf.get_rect(center=(self.x_center, y)))
            y += font.get_linesize()
