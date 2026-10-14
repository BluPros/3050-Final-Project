import pygame
from enum import Enum


def GameState():
    MENU = 0,
    PLAYING = 1,
    PAUSE = 2,
    GAME_OVER = 3


class GameStateManger:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Game State Manager")

        self.current_state = GameState.MENU

    def start(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events():
        pass

    def update():
        pass
