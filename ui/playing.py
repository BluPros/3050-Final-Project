import pygame
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
from pygame_widgets.button import Button
import constants

class PlayingOverlay:
    def __init__(self, screen, on_exit, game):
        self.surface = screen
        self.on_exit = on_exit
        self.game = game
        self.players = []
        self.widgets = []
        self.deploy_widgets = []
        self.deploy_troop_counter = 0
        self.attack_widgets = []
        self.attack_troop_counter = 0
        self.fortify_widgets = []
        self.fortify_troop_counter = 0
        self.create_widgets()
        self.hide_widgets(self.widgets + self.deploy_widgets + self.attack_widgets + self.fortify_widgets)
        self.error_popup = ErrorPopUp(
            self.surface,
            on_close=self.show_widgets
        )
        self.confirmation_popup = ConfirmationPopUp(
            self.surface,
            on_close=self.show_widgets
        )


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
                   text="Help", onClick=self.end_phase,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]

        # Deployment Phase widgets
        self.deploy_widgets =[
            # Deploy Troops button
            Button(self.surface, 830, 386, constants.PANEL_WIDTH - 40, 40,
                   text="Deploy Troops", onClick=self.end_phase,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 316, 40, 40,
                   text="-", onClick=self.remove_deployment_troop,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 316, 40, 40,
                   text="+", onClick=self.add_deployment_troop,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]
        # Attack Phase widgets

        # Fortify Phase widgets

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

    def remove_deployment_troop(self):
        if self.deploy_troop_counter > 0:
            self.deploy_troop_counter -= 1

    def add_deployment_troop(self):
        player = self.game.current_player

        if player is None:
            return

        if self.deploy_troop_counter < player.reinforcements:
            self.deploy_troop_counter += 1

    def configure_player_cards(self, players):
        player_x_coordinates = constants.CARD_X_POSITIONS.get(len(players), [])
        for player, x in zip(players, player_x_coordinates):
            player.x_center = x

    def draw(self, surface):
        # Title
        font = pygame.font.SysFont(constants.FONT_STYLE, 30)
        text_surface = font.render("Playing Screen", True, constants.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (640, 30)
        surface.blit(text_surface, text_rect)

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
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.CLAIM_COLOR, background_rect, border_radius=8
        )
        # Selected territory box
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20 , constants.PANEL_Y_TOP + 240, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius = 8
        )
        # Title
        self.draw_text(
            message="Claim Territory",
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
        if step == "claim":
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
        elif step == "place":
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
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.DEPLOY_COLOR, background_rect, border_radius=8
        )

        # Selected terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 128, constants.PANEL_WIDTH - 40, 128
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
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
            message=f"{player.reinforce}",
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


    def draw_attack(self, player):
        # Background Rectangle

        # Attacking from rectangle

        # Defending terr. rectangle

        # Title

        # Player name

        # "Attacking from" text

        # Attacking from territory name

        # Attacking from territory troop count

        # "Defending Territory" Text

        # Defending territory name

        # Defending territory troop count

        # "Attacking troops" text

        # Attacking troops counter

        pass

    def draw_fortify(self, player):
        # Background rectangle

        # Moving From rectangle

        # Moving to rectangle

        # Title

        # Player Name

        # "Moving from" text

        # Moving from territory name

        # Moving from terr. troop count

        # "Moving to" Text

        # Moving to terr. name

        # Moving from terr. troop count

        # "Troops to Move" text

        # troops to move counter

        pass

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

    def end_phase(self):
        pass
