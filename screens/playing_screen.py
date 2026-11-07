import pygame
import constants
import random
from ui.map_screen import MapScreen
from screens.base_screen import Screen
from game.game_state import Game
from ui.playing import PlayingOverlay

# Playing Screen


class PlayingScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)

        # Create the game object to store the state of the game, including players and territories
        self.game = Game()

        # Create the playing overlay
        self.playing_overlay = PlayingOverlay(screen=manager.screen, on_exit=manager.go_back, game=self.game)
        self.widgets = self.playing_overlay.widgets
        self.deploy_widgets = self.playing_overlay.deploy_widgets

        # TESTING FOR OWNERSHIP OVERLAY

        self.game.add_player(
            "Player 1",
            constants.PLAYER_RED
        )

        self.game.add_player(
            "Player 2",
            constants.PLAYER_BLUE,
            is_bot=True
        )
        # Temporary players for testing
        self.game.add_player(
            "Player 3",
            constants.PLAYER_GREEN,
            is_bot=True
        )

        self.game.add_player(
            "Player 4",
            constants.PLAYER_YELLOW,
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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            player = self.game.current_player

            # Only human players use mouse clicks
            if player is not None and not player.is_bot:

                territory = self.map_screen.get_territory_at(event.pos)

                if territory is not None:

                    if self.game.phase == "setup_claim":

                        claimed = self.game.claim_territory(territory.name)

                        if claimed:
                            self.map_screen.rebuild_ownership_overlay()
                            self.last_bot_action = pygame.time.get_ticks()

                            print(
                                f"{player.name} claimed {territory.name}"
                            )

                    elif self.game.phase == "setup_place":

                        placed = self.game.place_setup_army(territory.name)

                        if placed:
                            self.last_bot_action = pygame.time.get_ticks()

                            print(
                                f"{player.name} placed an army on {territory.name}"
                            )

        # Temporary keyboard control for normal turns
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            if self.game.game_started and self.game.phase != "game_over":
                self.game.next_phase()

                print(
                    f"Current player: {self.game.current_player.name} | "
                    f"Phase: {self.game.phase}"
                )

    def draw(self, surface):
        # Draw the background
        surface.fill(constants.BACKGROUND_COLOR)
        # Draw the map
        self.map_screen.draw(surface)
        # Draw the overlay
        self.playing_overlay.draw(surface)
        for player in self.game.players:
            player.draw(surface)
        # Draw the phase panel
        match self.game.phase:
            case "setup_claim":
                self.playing_overlay.draw_setup(self.game.current_player, "claim", self.map_screen.hovered_territory)
            case "setup_place":
                self.playing_overlay.draw_setup(self.game.current_player, "place", self.map_screen.hovered_territory)
            case "deploy":
                self.playing_overlay.draw_deploy(self.game.current_player)
            case "attack":
                self.playing_overlay.draw_attack(self.game.current_player)
            case "fortify":
                self.playing_overlay.draw_fortify(self.game.current_player)

    def update(self):
        self.map_screen.update()

        # Bots act during both setup phases
        if self.game.phase not in ("setup_claim", "setup_place"):
            return

        player = self.game.current_player

        # Human players control their own turns
        if player is None or not player.is_bot:
            return

        current_time = pygame.time.get_ticks()

        # Wait one second between bot actions
        if current_time - self.last_bot_action < self.bot_delay:
            return

        if self.game.phase == "setup_claim":

            # Find territories that have not been claimed
            available_territories = [
                territory.name
                for territory in self.game.territories.values()
                if territory.owner_id is None
            ]

            if not available_territories:
                return

            territory_name = random.choice(available_territories)

            claimed = self.game.claim_territory(territory_name)

            if claimed:
                self.map_screen.rebuild_ownership_overlay()

                print(
                    f"{player.name} claimed {territory_name}"
                )

        elif self.game.phase == "setup_place":

            # Find territories owned by the current bot
            owned_territories = [
                territory.name
                for territory in self.game.territories.values()
                if territory.owner_id == player.player_id
            ]

            if not owned_territories:
                return

            territory_name = random.choice(owned_territories)

            placed = self.game.place_setup_army(territory_name)

            if placed:
                print(
                    f"{player.name} placed an army on {territory_name}"
                )

                print(
                    f"Remaining armies: "
                    f"{self.game.setup_armies[player.player_id]}"
                )

        # Restart the timer after the bot action
        self.last_bot_action = current_time

    def on_enter(self):
        for widget in self.widgets:
            widget.show()