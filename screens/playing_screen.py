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
        self.playing_overlay = PlayingOverlay(screen=manager.screen, on_exit=manager.go_back)
        self.widgets = self.playing_overlay.widgets

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

        self.dice_font = pygame.font.Font(None, 28)

        self.roll_button_rect = pygame.Rect(680, 620, 160, 45)

        self.game.start_setup()

        self.attacker_rolls = []
        self.defender_rolls = []
        self.dice_error = ""

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if self.roll_button_rect.collidepoint(event.pos):
                print("Roll Dice button clicked")
                return

    def draw(self, surface):
        # Clear the previous frame before drawing anything else
        surface.fill(constants.BACKGROUND_COLOR)

        # Draw the map
        self.map_screen.draw(surface)

        # Draw the existing game overlay and player information
        self.playing_overlay.draw(surface)

        for player in self.game.players:
            player.draw(surface)

        # Draw the dice panel after the other screen elements
        pygame.draw.rect(
            surface,
            (221, 191, 138),
            pygame.Rect(820, 60, 250, 250),
            border_radius=8,
        )

        # Draw the attacker's stored dice results
        for index, value in enumerate(self.attacker_rolls):
            self.draw_die(
                surface,
                value,
                840 + index * 60,
                100,
                color=(220, 90, 90),
            )

        # Draw the defender's stored dice results
        for index, value in enumerate(self.defender_rolls):
            self.draw_die(
                surface,
                value,
                840 + index * 60,
                170,
                color=(235, 235, 235),
            )

        # Draw the Roll Dice button
        pygame.draw.rect(
            surface,
            (139, 100, 65),
            self.roll_button_rect,
            border_radius=6,
        )

        # Center the label inside the button
        label = self.dice_font.render(
            "Roll Dice",
            True,
            (0, 0, 0),
        )

        surface.blit(
            label,
            label.get_rect(center=self.roll_button_rect.center),
        )

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

    def draw_die(self, surface, value, x, y, size=50, color=(240, 240, 240)):
        if value not in range(1, 7):
            raise ValueError("Die value must be between 1 and 6.")

        # Define the die's position and dimensions
        rect = pygame.Rect(x, y, size, size)

        # Draw the die's background with rounded corners
        pygame.draw.rect(surface, color, rect, border_radius=8)

        # Draw a dark outline around the die
        pygame.draw.rect(
            surface,
            (30, 30, 30),
            rect,
            width=2,
            border_radius=8,
        )

        # Define the dot locations for each possible die value.
        pip_positions = {
            1: [(1, 1)],
            2: [(0, 0), (2, 2)],
            3: [(0, 0), (1, 1), (2, 2)],
            4: [(0, 0), (2, 0), (0, 2), (2, 2)],
            5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
            6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)],
        }

        # Convert the grid positions into pixel offsets inside the die
        # Dots sit at one-quarter, one-half, or three-quarters of its size
        offsets = [size // 4, size // 2, 3 * size // 4]

        # Draw only the dots needed for the current die value.
        for column, row in pip_positions[value]:
            # Add the die's screen position to the dot's internal offsets.
            center = (x + offsets[column], y + offsets[row])

            # Scale the dot radius with the die size, with a minimum of 2 pixels.
            pygame.draw.circle(
                surface,
                (20, 20, 20),
                center,
                max(2, size // 12),
            )