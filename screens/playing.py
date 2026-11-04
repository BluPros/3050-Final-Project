import pygame
import constants
import random
from ui.map_screen import MapScreen
from Screens.base_screen import Screen
from game.game_state import Game

# Playing Screen


class PlayingScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)

        # Create the game object to store the state of the game, including players and territories
        self.game = Game()

        # Temporary players for testing
        self.game.add_player(
            "Player 1",
            constants.PLAYER_RED
        )

        self.game.add_player(
            "Player 2",
            constants.PLAYER_BLUE,
            is_bot=True
        )

        self.game.start_setup()

        print("Game started")
        print("Current player:", self.game.current_player.name)
        print("Current phase:", self.game.phase)

        self.map_screen = MapScreen(
            constants.VISIBLE_MAP,
            constants.MASK_MAP,
            self.game
        )
        # Delay between bot actions in milliseconds
        self.bot_delay = 1000

        # Record the time of the last bot action to add delay to the next bot action
        self.last_bot_action = pygame.time.get_ticks()


    def handle_event(self, event):
        self.map_screen.handle_click(event)

        # Territory claiming with the mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Only allow human players to claim territories
            player = self.game.current_player

            if player is not None and not player.is_bot:

                territory = self.map_screen.get_territory_at(event.pos)

                if territory is not None:
                    claimed = self.game.claim_territory(territory.name)

                    if claimed:
                        self.map_screen.rebuild_ownership_overlay()

                        # Record the time of the last bot action for potential bot turn management
                        self.last_bot_action = pygame.time.get_ticks()

                        print(
                            f"{player.name} claimed {territory.name}"
                        )

        # Temporary use of space to advance turns before we have the button implemented by tre
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            if self.game.game_started:
                self.game.next_phase()

                print(
                    f"Current player: {self.game.current_player.name} | "
                    f"Phase: {self.game.phase}"
                )

    def draw(self, surface):
        self.map_screen.draw(surface)

    def update(self):
        self.map_screen.update()

        # Bots only act during territory claiming for now will try to implement fully this sprint
        if self.game.phase != "setup_claim":
            return

        player = self.game.current_player

        if player is None or not player.is_bot:
            return

        current_time = pygame.time.get_ticks()

        # Potentially how we want to delay the bots action so that it is visible to human players
        if current_time - self.last_bot_action < self.bot_delay:
            return

        # Right now the bot will randomly choose available territories and claim them during setup
        available_territories = [
            territory.name
            for territory in self.game.territories.values()
            if territory.owner_id is None
        ]

        if not available_territories:
            return

        # Randomly choose one available territory
        territory_name = random.choice(available_territories)

        claimed = self.game.claim_territory(territory_name)

        if claimed:
            self.map_screen.rebuild_ownership_overlay()
            self.last_bot_action = current_time

            print(
                f"{player.name} claimed {territory_name}"
            )
