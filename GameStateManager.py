import constants
import pygame
import sys
from screens import base_screen, menu, playing, instructions
import pygame_widgets


class GameStateManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Game State Manager")
        self.clock = pygame.time.Clock()

        # All available game states/screens
        self.screens = {
            "menu": menu.MenuScreen(self, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT),
            "playing": playing.PlayingScreen(self, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT),
            "instructions": instructions.InstructionScreen(self, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
            # "help": HelpScreen(self)
        }
        # On Init Default Screen is "menu"
        self.current_screen = self.screens["menu"]
        self.previous_screen = None
        self.current_screen.on_enter()

    def change_screen(self, name):
        # Update which screen is active (widgets)
        self.current_screen.on_exit()
        # Update prev. screen
        self.previous_screen = self.current_screen
        # Change screen for manager
        self.current_screen = self.screens[name]
        # Show new current widgets
        self.current_screen.on_enter()
        
    def go_back(self):
        # check that prev screen exists
        if self.previous_screen is None:
            return
        # exit current screen
        self.current_screen.on_exit()
        # switch current and prev screen
        self.current_screen, self.previous_screen = self.previous_screen, self.current_screen
        # enter next
        self.current_screen.on_enter()

    def start(self):
        while True:
            # optional delta time var
            # dt = self.clock.tick(60) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
                self.current_screen.handle_event(event)
            self.current_screen.update()
            self.screen.fill(constants.BLACK)
            self.current_screen.draw(self.screen)
            pygame_widgets.update(events) # Ensures widgets render on top
            pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_state_manager = GameStateManager()
    game_state_manager.start()
