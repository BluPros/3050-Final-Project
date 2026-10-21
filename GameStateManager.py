import constants
import pygame
import sys
import screens.menu as menu
from enum import Enum
from elements import Button


class GameStateManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Game State Manager")
        self.clock = pygame.time.Clock()

        # All available game states/screens
        self.screens = {
            "menu": menu.MenuScreen(self, constants.WINDOW_WIDTH),
            # "playing": PlayingScreen(self),
            # "help": HelpScreen(self)
        }
        # On Init Default Screen is "menu"
        self.current_screen = self.screens["menu"]

    def change_screen(self, name):
        self.current_screen = self.screens[name]

    def start(self):
        while True:
            # optional delta time var
            # dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                self.current_screen.handle_event(event)
            self.current_screen.update()
            self.screen.fill(constants.BLACK)
            self.current_screen.draw(self.screen)
            pygame.display.flip()

    def quit_game():
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_state_manager = GameStateManager()
    game_state_manager.start()
