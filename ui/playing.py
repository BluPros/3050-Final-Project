import pygame
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
from pygame_widgets.button import Button
from constants import *

class PlayingOverlay:
    def __init__(self, screen, on_exit):
        self.surface = screen
        self.on_exit = on_exit
        self.players = []
        self.bots = []
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
                   text="End Phase", onClick=self.end_phase(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # Help Menu Button
            Button(self.surface, 980, 670, 140, 40,
                   text = "Help", onClick=self.end_phase(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
        ]
        return widgets

    def hide_widgets(self):
        for widget in self.widgets:
            widget.hide()

    def show_widgets(self):
        for widget in self.widgets:
            widget.show()

    def draw(self, surface):
        # Title
        font = pygame.font.SysFont("georgia", 52)
        text_surface = font.render("Player Initiation", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (640, 80)
        surface.blit(text_surface, text_rect)

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

    def end_phase(self):
        pass