import pygame
from constants import *
from pygame_widgets.button import Button
from Screens.base_screen import Screen


# Menu Screen
# TODO: add title/background

class NewGameMenu:
    def __init__(self, screen, on_exit):
        self.screen = screen
        ## on_exit is a lambda function passed in through init
        ## should call the change menu on the last screen we were on
        self.on_exit = on_exit
        self.players = []
        self.bots = []
        self.error_message = None
        self.running = False
        self.visible = False
        self.widgets = self.create_widgets()

    def create_widgets(self):
        buttons = [
            # remove player button
            Button(self.screen, 220, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_player(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Player Button
            Button(self.screen, 380, 220, 40, 40,
                   text="+", onClick=lambda: self.add_player(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR)
            # remove Bot Button

            # add Bot Button

            # Back Button

            # Confirm Button
        ]
        return buttons

    def add_player(self):
        pass

    def remove_player(self):
        pass

    def add_bot(self):
        pass

    def remove_bot(self):
        pass

    def draw(self, surface):
        pass
