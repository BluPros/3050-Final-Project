import pygame
import constants
from ui.map_screen import MapScreen
from screens.base_screen import Screen
from game.game_state import Game

# Playing Screen


class PlayingScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)

        # Create the game object to store the state of the game, including players and territories
        self.game = Game()

        # TESTING FOR OWNERSHIP OVERLAY

        player1 = self.game.add_player(
            "Player 1",
            constants.PLAYER_RED
        )

        player2 = self.game.add_player(
            "Player 2",
            constants.PLAYER_BLUE
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
            constants.VISIBLE_MAP,
            constants.MASK_MAP,
            self.game
        )


    def handle_event(self, event):
        self.map_screen.handle_click(event)

    def draw(self, surface):
        self.map_screen.draw(surface)

    def update(self):
        self.map_screen.update()
