import constants
import pygame
import sys
from enum import Enum
from elements import Button


class GameState:
    MENU = 0,
    PLAYING = 1,
    PAUSE = 2,
    HELP = 3,
    GAME_OVER = 4

# TODO:
# - import each window (menu.py, instructions,py, etc.)
# - allow butt-click to change active game_state


class GameStateManger:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        pygame.display.set_caption("Game State Manager")

        self.current_state = GameState.MENU

    def start(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

    def handle_menu_input(self):
        pass

    def handle_gameplay_input(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.GAMEPLAY:
            self.render_gameplay()
        elif self.current_state == GameState.PAUSE:
            self.render_pause()
        elif self.current_state == GameState.GAME_OVER:
            self.render_game_over()

        pygame.display.flip()

    def render_menu(self):
        button_width = 200
        center_x = (constants.WINDOW_WIDTH - button_width) // 2

        def start_game():
            pass

        def quit_game():
            sys.exit()

        buttons = [
            Button("Play", center_x, 220, button_width, 60,
                   start_game, constants.LIGHT_BLUE, constants.WHITE),
            Button("Quit", center_x, 320, button_width, 60,
                   quit_game, constants.LIGHT_BLUE, constants.WHITE)
        ]
        for button in buttons:
            button.draw(self.screen)

    def render_gameplay(self):
        pass

    def render_pause(self):
        pass

    def render_help(self):
        pass

    def render_game_over(self):
        pass

    def quit_game(self):
        pygame.quit()
        quit()


if __name__ == "__main__":
    game_state_manager = GameStateManger()
    game_state_manager.start()
