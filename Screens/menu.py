import pygame
import constants
from elements import Button

# Menu Screen
# TODO: Discard elements usage, use pre-built buttons from:
# from pygame_widgets.button import ButtonArray


class MenuScreen:
    def __init__(self, manager, window_width):
        self.manager = manager
        # Button Vars
        button_width = 200
        center_x = (window_width - button_width) // 2
        # Active screen buttons
        self.buttons = [
            Button("Play", center_x, 200, button_width, 60,
                   lambda: manager.change_screen("playing"), constants.LIGHT_BLUE, constants.WHITE),
            Button("Quit", center_x, 300, button_width, 60,
                   manager.quit_game, constants.LIGHT_BLUE, constants.WHITE)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                button.click(event.pos)

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)
        # Draw rest of menu here

        # text_surface = font.render

    def update(self):
        pass
