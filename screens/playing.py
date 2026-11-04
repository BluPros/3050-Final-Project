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

        # Temporary players for testing
        player1 = self.game.add_player(
            "Player 1",
            constants.PLAYER_RED
        )

        player2 = self.game.add_player(
            "Player 2",
            constants.PLAYER_BLUE
        )
        
        # Different troop counts to test how numbers fit inside the circles
        test_troop_counts = [
            1,
            2,
            5,
            9,
            10,
            15,
            25,
            50,
            99
        ]

        # Temporarily assign every territory to a player for testing
        for index, territory_name in enumerate(self.game.territories):

            # Alternate between the two players
            player = self.game.players[
                index % len(self.game.players)
            ]

            # Cycle through the different troop counts
            troop_count = test_troop_counts[
                index % len(test_troop_counts)
            ]

            self.game.assign_territory(
                territory_name,
                player.player_id,
                troops=troop_count
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
