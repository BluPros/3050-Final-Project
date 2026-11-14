import pygame
from pygame_widgets.button import Button

import constants
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
import random

class PlayingOverlay:
    """Manages the playing screen, including widgets, popups, and game state tracking."""
    def __init__(
            self, screen, on_exit, game, on_end_phase=None,
            on_help=None, on_deploy=None, on_fortify=None,
            on_attack=None, on_cards=None):
        self.surface = screen
        self.on_exit = on_exit
        self.game = game
        self.on_end_phase = on_end_phase
        self.on_help = on_help
        self.on_deploy = on_deploy
        self.on_fortify = on_fortify
        self.on_attack = on_attack
        self.on_cards = on_cards
        self.players = []
        self.widgets = []
        self.deploy_widgets = []
        self.deploy_troop_counter = 0
        self.attack_widgets = []
        self.attack_troop_counter = 0
        self.fortify_widgets = []
        self.fortify_troop_counter = 0

        # Track dice popups
        self.dice_popup = False
        self.dice_rolling = False
        self.dice_started = 0
        self.dice_duration = 900
        self.dice_last_frame = -1
        self.dice_random = random.Random()

        # Store the displayed rolls and actual result
        self.attacker_faces = []
        self.defender_faces = []
        self.dice_result = None
        self.dice_source = ""
        self.dice_destination = ""
        self.dice_message = ""

        # Track selected territories
        self.selected_src = None
        self.selected_dst = None

        # Track movement after conquering territories
        self.moving_in = False
        self.map_limbo = False

        self.create_widgets()

        self.hide_widgets(
            self.widgets
            + self.deploy_widgets
            + self.attack_widgets
            + self.fortify_widgets
            )

        self.error_popup = ErrorPopUp(
            self.surface,
            on_close=self.show_widgets
        )
        self.confirmation_popup = ConfirmationPopUp(
            self.surface,
            on_close=self.show_widgets
        )

    def clear_selection(self):

        # Reset troop counters
        self.deploy_troop_counter = 0
        self.attack_troop_counter = 0
        self.fortify_troop_counter = 0

        # maintains clicked order for battle, move, fortify, etc.
        self.selected_src = None
        self.selected_dst = None

        # true after conquest, until confirms move-in
        self.moving_in = False

        # if owners are changing
        self.map_limbo = False

    def create_widgets(self):
        # Regular Buttons that show all the time.
        self.widgets =[
            # End Phase button
            Button(self.surface, 810, 440, constants.PANEL_WIDTH, 40,
                   text="End Phase", onClick=self.end_phase,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),

            # Help Menu Button
            Button(self.surface, 10, 10, 140, 40,
                   text="Help", onClick=self.show_help,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),

            # Cards Menu Button
            Button(
                    self.surface, 810, 510, 180, 147,
                    text="Cards",
                    onClick=self.show_cards,
                    inactiveColour=constants.BUTTON_COLOR,
                    pressedColour=constants.WHITE,
                    hoverColour=constants.BUTTON_HOVER_COLOR
                )
        ]

        # Deployment Phase widgets
        self.deploy_widgets =[
            # Deploy Troops button
            Button(
                    self.surface, 830, 386,
                    constants.PANEL_WIDTH - 40, 40,
                    text="Deploy Troops",
                    onClick=self.deploy_troops,
                    inactiveColour=constants.BUTTON_COLOR,
                    pressedColour=constants.WHITE,
                    hoverColour=constants.BUTTON_HOVER_COLOR
                ),
            # Remove troop button
            Button(
                self.surface,
                constants.PANEL_X_CENTER - 70, 316, 40, 40,
                text="-",
                onClick=self.remove_deployment_troop,
                inactiveColour=constants.BUTTON_COLOR,
                pressedColour=constants.WHITE,
                hoverColour=constants.BUTTON_HOVER_COLOR
            ),
            # Add Troop button
            Button(
                self.surface,
                constants.PANEL_X_CENTER + 30, 316, 40, 40,
                text="+",
                onClick=self.add_deployment_troop,
                inactiveColour=constants.BUTTON_COLOR,
                pressedColour=constants.WHITE,
                hoverColour=constants.BUTTON_HOVER_COLOR
            )
        ]
        # Attack Phase widgets
        self.attack_widgets = [
            # Deploy Troops button
            Button(self.surface, 830, 390, constants.PANEL_WIDTH - 40, 40,
                   text="Initiate Attack", onClick=self.initiate_attack,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 340, 40, 40,
                   text="-", onClick=self.remove_attack_troop,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 340, 40, 40,
                   text="+", onClick=self.add_attack_troop,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]
        # Fortify Phase widgets
        self.fortify_widgets = [
            # Deploy Troops button
            Button(self.surface, 830, 390, constants.PANEL_WIDTH - 40, 40,
                   text="Move Troops", onClick=self.fortify_troops,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 340, 40, 40,
                   text="-", onClick=self.remove_fortify_troop,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 340, 40, 40,
                   text="+", onClick=self.add_fortify_troop,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]

    # Hides all the widgets we don't want to see
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.hide()

    # Optionally takes a list of widgets that we want to show.
    def show_widgets(self, widgets=None):
        if widgets is None:
            widgets = self.widgets

        for widget in widgets:
            widget.show()

    # Hide the widgets and show only the ones we need for this phase
    def update_phase_widgets(self):
        self.hide_widgets(
            self.deploy_widgets + self.attack_widgets + self.fortify_widgets
        )

        match self.game.phase:
            case "deploy":
                self.show_widgets(self.deploy_widgets)
            case "attack":
                self.show_widgets(self.attack_widgets)
            case "fortify":
                self.show_widgets(self.fortify_widgets)

    def select_territory(self, territory):
        player = self.game.current_player
        owned = territory.owner_id == player.player_id

        if self.game.phase == "deploy":
            if owned:
                self.selected_src = territory

        elif self.game.phase == "attack":
            if self.moving_in:
                return
            if owned and territory.troops >= 2:
                self.selected_src = territory
                self.selected_dst = None
                self.attack_troop_counter = min(3, territory.troops - 1)
            elif not owned and self.selected_src and self.selected_src.is_neighbor(territory.name):
                self.selected_dst = territory

        elif self.game.phase == "fortify":
            if not owned:
                return
            if territory is self.selected_src:
                self.clear_selection()
            elif self.selected_src is None:
                self.selected_src = territory
            else: self.selected_dst = territory

    def remove_deployment_troop(self):
        if self.deploy_troop_counter > 0:
            self.deploy_troop_counter -= 1

    def add_deployment_troop(self):
        player = self.game.current_player

        if player is None:
            return

        if self.deploy_troop_counter < player.reinforcements:
            self.deploy_troop_counter += 1

    def deploy_troops(self):
        if self.on_deploy is not None:
            self.on_deploy()

    def remove_attack_troop(self):
        if self.moving_in:
            minimum = self.game.pending_conquest["min_move"]
        else:
            minimum = 1

        if self.attack_troop_counter > minimum:
            self.attack_troop_counter -= 1


    def add_attack_troop(self):
        src = self.selected_src
        if src is None:
            return

        if self.moving_in:
            limit = src.troops -1
        else:
            limit = min(3, src.troops -1)

        if self.attack_troop_counter < limit:
            self.attack_troop_counter += 1

    def initiate_attack(self):
        if self.moving_in:
            if self.on_attack is not None:
                self.on_attack()
            return

        self.show_dice()

    def remove_fortify_troop(self):
        if self.fortify_troop_counter > 0:
            self.fortify_troop_counter -= 1

    def add_fortify_troop(self):
        territory = self.selected_src

        if territory is None:
            return

        if self.fortify_troop_counter < territory.troops - 1:
            self.fortify_troop_counter += 1

    def fortify_troops(self):
        if self.on_fortify is not None:
            self.on_fortify()

    def configure_player_cards(self, players):
        player_x_coordinates = constants.CARD_X_POSITIONS.get(len(players), [])
        for player, x in zip(players, player_x_coordinates):
            player.x_center = x

    def draw(self, surface):
        if surface is None:
            surface = self.surface

        # Background banner
        background_rect = pygame.Rect(
            constants.BANNER_X_LEFT,
            constants.BANNER_Y_TOP,
            constants.BANNER_WIDTH,
            constants.BANNER_HEIGHT
        )
        pygame.draw.rect(surface, constants.BUTTON_COLOR, background_rect)

        match self.game.phase:
            case "deploy":
                deploy_rect = pygame.Rect(
                    constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 2,
                    constants.BANNER_Y_TOP + 5,
                    constants.BANNER_WIDTH // 6 - 5,
                    constants.BANNER_HEIGHT - 10
                )
                pygame.draw.rect(surface, constants.DEPLOY_COLOR, deploy_rect)
            case "attack":
                attack_rect = pygame.Rect(
                    constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 3 * 2,
                    constants.BANNER_Y_TOP + 5,
                    constants.BANNER_WIDTH // 6 - 5,
                    constants.BANNER_HEIGHT - 10
                )
                pygame.draw.rect(surface, constants.ATTACK_COLOR, attack_rect)
            case "fortify":
                fortify_rect = pygame.Rect(
                    constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 6 * 5,
                    constants.BANNER_Y_TOP + 5,
                    constants.BANNER_WIDTH // 6 - 5,
                    constants.BANNER_HEIGHT - 10
                )
                pygame.draw.rect(surface, constants.FORTIFY_COLOR, fortify_rect)
        # Current player name
        self.draw_text(
            message=self.game.current_player.name,
            x=constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 4,
            y=constants.BANNER_Y_TOP + constants.BANNER_HEIGHT // 2,
            font_size=20,
            font_color=constants.TEXT_COLOR,
            )
        # Deploy, Attack, Fortify text
        self.draw_text(
            message="Deploy",
            x=constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 12 * 7,
            y=constants.BANNER_Y_TOP + constants.BANNER_HEIGHT // 2,
            font_size=20,
            font_color=constants.TEXT_COLOR,
        )
        self.draw_text(
            message="Attack",
            x=constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 4 * 3,
            y=constants.BANNER_Y_TOP + constants.BANNER_HEIGHT // 2,
            font_size=20,
            font_color=constants.TEXT_COLOR,
        )
        self.draw_text(
            message="Fortify",
            x=constants.BANNER_X_LEFT + constants.BANNER_WIDTH // 12 * 11,
            y=constants.BANNER_Y_TOP + constants.BANNER_HEIGHT // 2,
            font_size=20,
            font_color=constants.TEXT_COLOR,
        )

    def draw_text(self, message, x, y, font_size, font_color=constants.TEXT_COLOR):
        # Make font object
        font = pygame.font.SysFont(constants.FONT_STYLE, font_size)
        # update the text
        text = font.render(message, True, font_color)
        # Write text to screen
        text_rect = text.get_rect(center=(x, y))
        self.surface.blit(text, text_rect)


    def draw_setup(self, player, step, hover_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT,
            constants.PANEL_Y_TOP,
            constants.PANEL_WIDTH,
            constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.CLAIM_COLOR, background_rect, border_radius=8
        )
        # Selected territory box
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 240,
            constants.PANEL_WIDTH - 40,
            100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius = 8
        )
        # Title
        self.draw_text(
            message=f"{step} Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=40,
            font_color=constants.TEXT_COLOR
        )

        # Draw Player Name
        self.draw_text(
            message=player.name,
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 110,
            font_size=24,
            font_color=constants.TEXT_COLOR
        )

        # Draw Instructions
        if step == "Claim":
            self.draw_text(
                message="Select an unclaimed territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 170,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )

            # Draw Selected Territory if one has been selected
            if hover_territory:
                self.draw_text(
                    message="Click to Claim:",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 270,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
                self.draw_text(
                    message=hover_territory.name,
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 310,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
            else:
                self.draw_text(
                    message="No territory selected.",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 295,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
        elif step == "Reinforce":
            self.draw_text(
                message="Select a territory you want to reinforce.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 170,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )

            # Draw Selected Territory if one has been selected
            if hover_territory:
                self.draw_text(
                    message="Click to Reinforce:",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 270,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
                self.draw_text(
                    message=hover_territory.name,
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 310,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
            else:
                self.draw_text(
                    message="No territory selected.",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 295,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )

    def draw_deploy(self, player, selected_territory=None):
        # Background rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT,
            constants.PANEL_Y_TOP,
            constants.PANEL_WIDTH,
            constants.PANEL_HEIGHT
        )

        pygame.draw.rect(
            self.surface,
            constants.DEPLOY_COLOR,
            background_rect,
            border_radius=8
        )

        # Selected territory rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 128,
            constants.PANEL_WIDTH - 40,
            128
        )

        pygame.draw.rect(
            self.surface,
            constants.WHITE,
            selected_terr_rect,
            border_radius=8
        )

        # Title
        self.draw_text(
            message="Deploy Troops",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player Name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops available text
        self.draw_text(
            message="Troops Available",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 90,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Actual Troops available
        self.draw_text(
            message=f"{player.reinforcements}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 110,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Selected territory and number of troops on that territory
        self.draw_text(
            message="Selected Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 160,
            font_size=24,
            font_color=constants.TEXT_COLOR
        )
        # Show the territory info if one has been selected, otherwise show none
        if selected_territory:
            self.draw_text(
                message=f"{selected_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 190,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )

            self.draw_text(
                message=f"Current Troops: {selected_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 220,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="No territory selected.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 190,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
        # Troops to deploy text
        self.draw_text(
            message="Troops to Deploy",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 280,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops to deploy counter
        self.draw_text(
            message=f"{self.deploy_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 320,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )


    def draw_attack(self, player, attacking_territory=None, defending_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT,
            constants.PANEL_Y_TOP,
            constants.PANEL_WIDTH,
            constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.ATTACK_COLOR, background_rect, border_radius=8
        )
        # Attacking From rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 80,
            constants.PANEL_WIDTH - 40,
            100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Defending terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 185,
            constants.PANEL_WIDTH - 40,
            100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Title
        self.draw_text(
            message="Attack",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # "Attacking from" text
        self.draw_text(
            message="Attacking From:",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 100,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Attacking Territory info if selected
        if attacking_territory:
            self.draw_text(
                message=f"{attacking_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Attacking from territory troop count
            self.draw_text(
                message=f"Current Troops: {attacking_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 165,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Defending Territory" Text
        self.draw_text(
            message="Defending Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 200,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Defending territory info if selected
        if defending_territory:
            self.draw_text(
                message=f"{defending_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Defending territory troop count
            self.draw_text(
                message=f"Current Troops: {defending_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 265,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Attacking troops" text
        self.draw_text(
            message="Attacking Troops",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 310,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Attacking troops counter
        self.draw_text(
            message=f"{self.attack_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 345,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )

    def draw_fortify(self, player, moving_from_territory, moving_to_territory):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT,
            constants.PANEL_Y_TOP,
            constants.PANEL_WIDTH,
            constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.FORTIFY_COLOR, background_rect, border_radius=8
        )
        # Attacking From rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 80,
            constants.PANEL_WIDTH - 40,
            100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Defending terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20,
            constants.PANEL_Y_TOP + 185,
            constants.PANEL_WIDTH - 40,
            100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Title
        self.draw_text(
            message="Fortify",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # "Moving from" text
        self.draw_text(
            message="Moving From:",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 100,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Moving from Territory info if selected
        if moving_from_territory:
            self.draw_text(
                message=f"{moving_from_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Moving from territory troop count
            self.draw_text(
                message=f"Current Troops: {moving_from_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 165,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Moving to Territory" Text
        self.draw_text(
            message="Moving to Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 200,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Moving to territory info if selected
        if moving_to_territory:
            self.draw_text(
                message=f"{moving_to_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Moving to territory troop count
            self.draw_text(
                message=f"Current Troops: {moving_to_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 265,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Troops to Move" text
        self.draw_text(
            message="Troops to Move",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 310,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops to move counter
        self.draw_text(
            message=f"{self.fortify_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 345,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

    def end_phase(self):
        if self.on_end_phase is not None:
            self.on_end_phase()

    def show_help(self):
        if self.on_help is not None:
            self.on_help()

    def show_cards(self):
        if self.on_cards is not None:
            self.on_cards()

    # Opens the dice popup for the selected attack
    def show_dice(self):
        if self.dice_popup or self.game.phase != "attack":
            return

        if self.selected_src is None or self.selected_dst is None:
            return

        if not self.game.verify_attack(
            self.selected_src.name,
            self.selected_dst.name,
            self.attack_troop_counter
        ):
            return

        self.dice_popup = True
        self.dice_rolling = False
        self.dice_result = None
        self.attacker_faces = []
        self.defender_faces = []
        self.dice_source = self.selected_src.name
        self.dice_destination = self.selected_dst.name
        self.dice_message = "Click Roll to resolve this attack"
        self.hide_widgets(
            self.widgets + self.deploy_widgets
            + self.attack_widgets + self.fortify_widgets
        )


    # Closes the dice popup and restores the controls
    def close_dice(self):
        if self.dice_rolling:
            return

        self.dice_popup = False
        self.show_widgets(self.widgets)
        self.update_phase_widgets()


    # Resolves one attack using the existing callback
    def roll_dice(self):
        if not self.dice_popup or self.dice_rolling:
            return

        if self.dice_result is not None or self.on_attack is None:
            return

        # Clear old results before requesting a new attack
        self.game.clear_last_attack()
        self.on_attack()
        result = self.game.get_last_attack()

        if result is None:
            self.dice_message = "Attack could not be completed"
            return

        self.dice_result = result
        self.dice_started = pygame.time.get_ticks()
        self.dice_last_frame = -1
        self.dice_rolling = True
        self.dice_message = "Rolling dice"

        # Keep the movement counter valid after a conquest
        if self.game.pending_conquest is not None:
            self.attack_troop_counter = self.game.pending_conquest["min_move"]

        self.update_dice()


    # Updates the animation without making another attack
    def update_dice(self):
        if not self.dice_popup or not self.dice_rolling:
            return

        elapsed = pygame.time.get_ticks() - self.dice_started

        if elapsed >= self.dice_duration:
            self.attacker_faces = list(self.dice_result["attack_roll"])
            self.defender_faces = list(self.dice_result["defence_roll"])
            self.dice_rolling = False
            self.dice_message = (
                f"Attacker lost {self.dice_result['attacker_losses']} | "
                f"Defender lost {self.dice_result['defender_losses']}"
            )

            if self.dice_result["conquered"]:
                self.dice_message += " | Close to confirm troop movement"
            return

        frame = elapsed // 80
        if frame != self.dice_last_frame:
            self.dice_last_frame = frame

            # Temporary faces do not change the real game rolls
            self.attacker_faces = [
                self.dice_random.randint(1, 6)
                for _ in self.dice_result["attack_roll"]
            ]
            self.defender_faces = [
                self.dice_random.randint(1, 6)
                for _ in self.dice_result["defence_roll"]
            ]

    # Positions the dice controls inside the attack panel
    def dice_layout(self):
        self.dice_panel = pygame.Rect(
            constants.PANEL_X_LEFT,
            constants.PANEL_Y_TOP,
            constants.PANEL_WIDTH,
            constants.PANEL_HEIGHT
        )

        panel = self.dice_panel
        button_width = (panel.width - 60) // 2

        self.dice_roll_button = pygame.Rect(
            panel.left + 20,
            panel.bottom - 55,
            button_width,
            35
        )

        self.dice_close_button = pygame.Rect(
            panel.centerx + 10,
            panel.bottom - 55,
            button_width,
            35
        )


    # Handles popup input before the game controls
    def handle_dice_event(self, event):

        if not self.dice_popup:
            return False

        self.dice_layout()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close_dice()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.dice_close_button.collidepoint(event.pos):
                self.close_dice()
            elif self.dice_roll_button.collidepoint(event.pos):
                self.roll_dice()

        return event.type in (
            pygame.KEYDOWN, pygame.KEYUP, pygame.TEXTINPUT,
            pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION, pygame.MOUSEWHEEL
        )


    # Draws fitted text inside the dice popup
    def dice_text(self, text, center, size=20, max_width=None):
        font = pygame.font.SysFont(constants.FONT_STYLE, size)
        image = font.render(text, True, constants.TEXT_COLOR)

        if max_width and image.get_width() > max_width:
            height = max(1, int(image.get_height() * max_width / image.get_width()))
            image = pygame.transform.smoothscale(image, (max_width, height))

        self.surface.blit(image, image.get_rect(center=center))


    # Draws a die using dots
    def draw_die(self, rect, value, color):
        pygame.draw.rect(self.surface, color, rect, border_radius=8)
        pygame.draw.rect(self.surface, constants.TEXT_COLOR, rect, 2, border_radius=8)
        positions = {
            1: [(1, 1)],
            2: [(0, 0), (2, 2)],
            3: [(0, 0), (1, 1), (2, 2)],
            4: [(0, 0), (2, 0), (0, 2), (2, 2)],
            5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
            6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]
        }

        for column, row in positions[value]:
            center = (
                rect.left + rect.width * (column + 1) // 4,
                rect.top + rect.height * (row + 1) // 4
            )
            pygame.draw.circle(
                self.surface, constants.TEXT_COLOR, center,
                max(2, rect.width // 12)
            )


    # Draws the dice interface inside the attack panel
    def draw_dice_popup(self, surface):
        if not self.dice_popup:
            return

        self.surface = surface
        self.dice_layout()
        panel = self.dice_panel

        # Cover the normal attack panel
        pygame.draw.rect(
            surface,
            constants.ATTACK_COLOR,
            panel,
            border_radius=8
        )

        # Draw the panel title
        self.dice_text(
            "Attack Dice",
            (panel.centerx, panel.top + 30),
            28
        )

        # Draw the selected territories
        self.dice_text(
            "Attacking from",
            (panel.centerx, panel.top + 65),
            18
        )
        self.dice_text(
            self.dice_source,
            (panel.centerx, panel.top + 90),
            22,
            panel.width - 40
        )

        self.dice_text(
            "Defending territory",
            (panel.centerx, panel.top + 125),
            18
        )
        self.dice_text(
            self.dice_destination,
            (panel.centerx, panel.top + 150),
            22,
            panel.width - 40
        )

        # Position the attacker and defender dice
        centers = [
            panel.left + panel.width // 4,
            panel.left + panel.width * 3 // 4
        ]

        faces = [
            self.attacker_faces,
            self.defender_faces
        ]

        colors = [
            (225, 130, 115),
            (220, 230, 245)
        ]

        labels = [
            "Attacker",
            "Defender"
        ]

        # Fit three dice inside either half of the panel
        die_size = max(
            12,
            min(40, (panel.width // 2 - 40) // 3)
        )
        gap = 6

        for index, center_x in enumerate(centers):
            self.dice_text(
                labels[index],
                (center_x, panel.top + 195),
                18
            )

            count = len(faces[index])
            total_width = (
                count * die_size
                + max(0, count - 1) * gap
            )

            if count == 0:
                self.dice_text(
                    "Ready",
                    (center_x, panel.top + 235),
                    18
                )

            for die_index, value in enumerate(faces[index]):
                rect = pygame.Rect(
                    center_x - total_width // 2
                    + die_index * (die_size + gap),
                    panel.top + 215,
                    die_size,
                    die_size
                )

                self.draw_die(
                    rect,
                    value,
                    colors[index]
                )

        # Show a short result on separate lines
        if self.dice_rolling:
            lines = ["Rolling dice"]
        elif self.dice_result is not None:
            lines = [
                f"Attacker lost {self.dice_result['attacker_losses']}",
                f"Defender lost {self.dice_result['defender_losses']}"
            ]

            if self.dice_result["conquered"]:
                lines.append("Close to confirm troop movement")
        else:
            lines = [self.dice_message]

        for index, line in enumerate(lines):
            self.dice_text(
                line,
                (panel.centerx, panel.top + 285 + index * 23),
                18,
                panel.width - 30
            )

        # Draw the dice controls
        roll_enabled = (
            not self.dice_rolling
            and self.dice_result is None
        )
        close_enabled = not self.dice_rolling

        buttons = [
            (
                self.dice_roll_button,
                "Roll",
                roll_enabled
            ),
            (
                self.dice_close_button,
                "Close" if self.dice_result else "Cancel",
                close_enabled
            )
        ]

        for rect, label, enabled in buttons:
            color = (
                constants.BUTTON_COLOR
                if enabled
                else (145, 145, 145)
            )

            pygame.draw.rect(
                surface,
                color,
                rect,
                border_radius=5
            )

            self.dice_text(
                label,
                rect.center,
                20
            )
