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
        self.playing_overlay = PlayingOverlay(
            screen=manager.screen, 
            on_exit=manager.go_back,
            game=self.game,
            on_end_phase=self.advance_phase,
            on_help=lambda: manager.change_screen("instructions"),
            on_deploy=self.deploy_troops,
            on_fortify=self.fortify_troops,
            on_attack=self.initiate_attack)
        
        self.widgets = self.playing_overlay.widgets
        self.deploy_widgets = self.playing_overlay.deploy_widgets
        self.attack_widgets = self.playing_overlay.attack_widgets
        self.fortify_widgets = self.playing_overlay.fortify_widgets


        self.map_screen = MapScreen(
            constants.VISIBLE_MAP,
            constants.MASK_MAP,
            self.game
        )

        # Delay between bot actions in milliseconds
        self.bot_delay = constants.BOT_DELAY_MS

        # Record the time of the last bot action to add delay to the next bot action
        self.last_bot_action = pygame.time.get_ticks()


    def configure_game(self, player_settings):
        # Create a Game object for every new match
        self.game = Game()

        # Initialize player objects for the game given the player settings
        for settings in player_settings:
            self.game.add_player(
                settings["name"],
                settings["color"],
                is_bot=settings["is_bot"]
            )

        # Set up claiming and starting armies
        if not self.game.start_setup():
            raise ValueError("Game requires 3-6 players.")

        # Update the existing overlay to use the new game 
        self.playing_overlay.game = self.game
        self.playing_overlay.clear_selection()
        self.playing_overlay.map_limbo = False

        # Assign positions to the players cards
        self.playing_overlay.configure_player_cards(
            self.game.players
        )

        # Create a fresh map with the new territories so we dont update the hardcode values
        self.map_screen = MapScreen(
            constants.VISIBLE_MAP,
            constants.MASK_MAP,
            self.game
        )

        self.last_bot_action = pygame.time.get_ticks()
        self.last_phase = self.game.phase
        self.playing_overlay.update_phase_widgets()

        print("Starting new game:")
        for player in self.game.players:
            print(player.name, player.color, "Bot:", player.is_bot)

    # Advance the game to the next phase if possible
    def advance_phase(self):
        if not self.game.game_started:
            return

        if self.game.phase == "game_over":
            return

        previous_state = (
            self.game.phase,
            self.game.current_player_index
        )

        self.game.next_phase()

        current_state = (
            self.game.phase,
            self.game.current_player_index
        )

        if current_state != previous_state:
            self.playing_overlay.clear_selection()
            self.playing_overlay.update_phase_widgets()
            self.last_phase = self.game.phase
        else:
            print("Cannot advance phase yet.")
            
    def handle_event(self, event):

        # Test for end screen: Force Player 1 to win
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
            if self.game.players:
                self.game.winner_id = self.game.players[0].player_id
                self.game.phase = "game_over"
            return
        
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

                    elif self.game.phase in ("deploy", "attack", "fortify"):
                        self.playing_overlay.select_territory(territory)

        # Temporary keyboard control for normal turns
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            if self.game.game_started and self.game.phase != "game_over":
                self.advance_phase()

                print(
                    f"Current player: {self.game.current_player.name} | "
                    f"Phase: {self.game.phase}"
                )

        # Handle the Escape key to return to the menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.change_screen("menu")
            return
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
                self.playing_overlay.draw_setup(self.game.current_player, "Claim", self.map_screen.hovered_territory)
            case "setup_place":
                self.playing_overlay.draw_setup(self.game.current_player, "Reinforce", self.map_screen.hovered_territory)
            case "deploy":
                self.playing_overlay.draw_deploy(
                    self.game.current_player,
                    self.playing_overlay.selected_src
                )

            case "attack":
                self.playing_overlay.draw_attack(
                    self.game.current_player,
                    self.playing_overlay.selected_src,
                    self.playing_overlay.selected_dst
                )

            case "fortify":
                self.playing_overlay.draw_fortify(
                    self.game.current_player,
                    self.playing_overlay.selected_src,
                    self.playing_overlay.selected_dst
                )

    def update(self):
        self.map_screen.update()

        if self.game.phase != self.last_phase:
            self.last_phase = self.game.phase
            self.playing_overlay.clear_selection()
            self.playing_overlay.update_phase_widgets()

        if self.game.phase == "game_over":
            winner = self.game.get_player(self.game.winner_id)

            game_over_screen = self.manager.screens["game_over"]

            game_over_screen.set_winner(winner)

            self.manager.change_screen("game_over")
            return
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
        super().on_enter()

        self.playing_overlay.show_widgets(self.playing_overlay.widgets)

        self.last_bot_action = pygame.time.get_ticks()
        self.playing_overlay.on_enter()
        self.playing_overlay.update_phase_widgets()

    def on_exit(self):
        super().on_exit()
        self.playing_overlay.hide_widgets(
            self.playing_overlay.widgets
            + self.playing_overlay.deploy_widgets
            + self.playing_overlay.attack_widgets
            + self.playing_overlay.fortify_widgets
        )

    # Kind of awkward having this here, but since the playing screen has a game overlay
    # and a playing overlay, we need functions to communicate between the two.
    def deploy_troops(self):
        territory = self.playing_overlay.selected_src
        count = self.playing_overlay.deploy_troop_counter

        if territory is None or count <= 0:
            return

        successful_deployment = self.game.deploy(territory.name, count)

        if successful_deployment:
            self.playing_overlay.clear_selection()

    def initiate_attack(self):

        src = self.playing_overlay.selected_src
        dst = self.playing_overlay.selected_dst
        count = self.playing_overlay.attack_troop_counter

        if src is None or dst is None or count <= 0:
            return

        # First checking whether moving into a conquered territory or attacking
        # If conquering, move troops in.
        # If attacking, attack.
        if self.playing_overlay.moving_in:
            successful_move_in = self.game.move_in(count)
            if successful_move_in:
                self.playing_overlay.clear_selection()
                self.map_screen.rebuild_ownership_overlay()
                #Change attack button text back
                self.playing_overlay.attack_widgets[0].setText("Initiate Attack")
        else:
            attack_result = self.game.attack(src.name, dst.name, count)

            if attack_result is None:
                print("Bad attack")
            elif attack_result is False:
                print("Battle is over, but territory wasn't conquered.")
                # Have to update the attacking troops because the attacker lost troops?
                self.playing_overlay.attack_troop_counter = min(3, max(0, src.troops - 1))
            elif attack_result is True:
                print("Battle over and territory conquered.")
                self.playing_overlay.moving_in = True
                # Have to update troop counter to minimum number of troops to move into new territory
                self.playing_overlay.attack_troop_counter = (self.game.pending_conquest["min_move"])
                # Change attack button text
                self.playing_overlay.attack_widgets[0].setText("Confirm Move In")

    def fortify_troops(self):
        src = self.playing_overlay.selected_src
        dst = self.playing_overlay.selected_dst
        count = self.playing_overlay.fortify_troop_counter

        if src is None or dst is None or count <= 0:
            return

        successful_fortify = self.game.fortify(src.name, dst.name, count)

        if successful_fortify:
            self.playing_overlay.clear_selection()