import pygame
from constants import *
from ui.map_screen import MapScreen
from Screens.base_screen import Screen
from game.game_state import Game
from ui.playing import PlayingOverlay

# Playing Screen

class PlayingScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)

        # Create the game object to store the state of the game, including players and territories
        self.game = Game()

        # Create the playing overlay
        self.playing_overlay = PlayingOverlay(screen=manager.screen, on_exit=manager.go_back)
        self.widgets = self.playing_overlay.widgets

        # TESTING FOR OWNERSHIP OVERLAY

        player1 = self.game.add_player(
            "Player 1",
            PLAYER_RED
        )

        player2 = self.game.add_player(
            "Player 2",
            PLAYER_BLUE
        )
        self.game.assign_territory(
            "Alaska", 
            player1.player_id, 
            troops=5
        )

        self.game.assign_territory(
            "Northwest Territory",
            player1.player_id,
            troops=3
        )

        self.game.assign_territory(
            "Alberta",
            player2.player_id,
            troops=4
        )

        self.game.assign_territory(
            "Ontario",
            player2.player_id,
            troops=2
        )
        

        self.map_screen = MapScreen(
            VISIBLE_MAP,
            MASK_MAP,
            self.game
        )


    def handle_event(self, event):
        self.map_screen.handle_click(event)

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.map_screen.draw(surface)
        self.playing_overlay.draw(surface)

    def update(self):
        self.map_screen.update()

    def on_enter(self):
        for widget in self.widgets:
            widget.show()
