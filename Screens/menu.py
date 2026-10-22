import pygame
import constants
from pygame_widgets.button import Button

# Menu Screen
# TODO: Discard elements usage, use pre-built buttons from:
# from pygame_widgets.button import ButtonArray


class MenuScreen:
    def __init__(self, manager, window_width, window_height):
        self.manager = manager
        # Button Vars
        button_width = 200
        button_height = 60
        center_x = (window_width - button_width) // 2
        center_y = (window_height - button_height) // 2
        # Active screen buttons
        self.buttons = [
            Button(manager.screen, center_x - button_width, center_y, button_width, button_height, 
            text="Play", onClick=lambda: manager.change_screen("playing"), 
            inactiveColour=constants.LIGHT_BLUE, pressedColour=constants.WHITE),
            Button(manager.screen, center_x + button_width, center_y, button_width, button_height, 
            text="Quit", onClick=manager.quit_game, 
            inactiveColour=constants.LIGHT_BLUE, pressedColour=constants.WHITE)
        ]

    def handle_event(self, event):
        pass # pygame_widgets handle button clicks

    def draw(self, surface):
        pass # pygame_widgets draw the buttosn, draw title/background here

        # text_surface = font.render

    def update(self):
        pass
