import pygame
import constants
from ui.map_screen import MapScreen

# Playing Screen


class PlayingScreen:
    def __init__(self, manager, window_width, window_height):
        self.manager = manager
        self.map_screen = MapScreen(
            constants.VISIBLE_MAP,
            constants.MASK_MAP
        )

    def handle_event(self, event):
        self.map_screen.handle_click(event)

    def draw(self, surface):
        self.map_screen.draw(surface)

    def update(self):
        self.map_screen.update()
