import pygame
import constants
from ui.map_screen import MapScreen
from screens.base_screen import Screen

# Playing Screen


class PlayingScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)
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
