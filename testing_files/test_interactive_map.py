import sys
from pathlib import Path
SYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

import pygame

from ui.map_screen import MapScreen


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 533

VISIBLE_MAP = SYSTEM_ROOT / "assets" / "maps" / "risk_map_original.png"
MASK_MAP = SYSTEM_ROOT / "assets" / "maps" / "risk_map_mask.png"


def main():

    pygame.init()

    # Creates the game window
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("Risk")

    # Variable to change game fps
    clock = pygame.time.Clock()

    map_screen = MapScreen(
        VISIBLE_MAP,
        MASK_MAP
    )

    running = True

    while running:

        for event in pygame.event.get():

            # Closes game if the user clicks the close button on the window
            if event.type == pygame.QUIT:
                running = False

            # Handle left clicks of territories
            map_screen.handle_click(event)

        map_screen.update()
        map_screen.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()