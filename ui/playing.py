import pygame
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
from pygame_widgets.button import Button
import constants

class PlayingOverlay:
    def __init__(self, screen, on_exit):
        self.surface = screen
        self.on_exit = on_exit
        self.players = []
        self.widgets = self.create_widgets()
        self.hide_widgets()
        self.error_popup = ErrorPopUp(
            self.surface,
            on_close=self.show_widgets
        )
        self.confirmation_popup = ConfirmationPopUp(
            self.surface,
            on_close=self.show_widgets
        )


    def create_widgets(self):
        widgets = [
            # End Phase Button
            Button(self.surface, 1130, 670, 140, 40,
                   text="End Phase", onClick=self.end_phase,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Help Menu Button
            Button(self.surface, 980, 670, 140, 40,
                   text = "Help", onClick=self.end_phase,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
        ]
        return widgets

    def hide_widgets(self):
        for widget in self.widgets:
            widget.hide()

    def show_widgets(self):
        for widget in self.widgets:
            widget.show()

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

    def draw_claim(self, player, hover_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.CLAIM_COLOR, background_rect
        )
        # Selected territory box
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20 , constants.PANEL_Y_TOP + 240, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect
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


    def draw_deploy(self, player):
        # Background Rectangle

        # Selected terr. rectangle

        # Title

        # Player Name

        # Troops available

        # Selected territory and number of troops on that territory

        # Troops to deploy text

        # Troops to deploy counter

        pass

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