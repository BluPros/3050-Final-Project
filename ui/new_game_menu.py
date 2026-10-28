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
        self.widgets = self.create_widgets()
        self.hide_widgets()

    def create_widgets(self):
        buttons = [
            # remove player button
            Button(self.screen, 220, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_player(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Player Button
            Button(self.screen, 380, 220, 40, 40,
                   text="+", onClick=lambda: self.add_player(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # remove Bot Button
            Button(self.screen, 860, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_bot(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Bot Button
            Button(self.screen, 1020, 220, 40, 40,
                   text="+", onClick=lambda: self.add_bot(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # Back Button
            Button(self.screen, 320, 640, 160, 60,
                   text="Back", onClick=lambda: self.on_exit(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # Confirm Button
            Button(self.screen, 800, 640, 160, 60,
                   text="Confirm", onClick=lambda: self.confirm(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
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
        surface.fill(BACKGROUND_COLOR)
        # Title
        font = pygame.font.SysFont("georgia", 52)
        text_surface = font.render("Player Initiation", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (640, 80)
        surface.blit(text_surface, text_rect)
        # Select # of Players
        font = pygame.font.SysFont("georgia", 24)
        text_surface = font.render("Select Number of Players", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (320, 160)
        surface.blit(text_surface, text_rect)
        # Select # of Bots
        font = pygame.font.SysFont("georgia", 24)
        text_surface = font.render("Select Number of Bots", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (960, 160)
        surface.blit(text_surface, text_rect)
        # Player count box and text
        player_box = pygame.Rect(290, 210, 60, 60)
        pygame.draw.rect(surface, PLAYER_ICON_COLOR, player_box)
        font = pygame.font.SysFont("georgia", 24)
        text_surface = font.render(f"{len(self.players)}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (320, 240)
        surface.blit(text_surface, text_rect)
        # Bot count box and text
        bot_box = pygame.Rect(930, 210, 60, 60)
        pygame.draw.rect(surface, BOT_ICON_COLOR, bot_box)
        font = pygame.font.SysFont("georgia", 24)
        text_surface = font.render(f"{len(self.bots)}", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (960, 240)
        surface.blit(text_surface, text_rect)

    def hide_widgets(self):
        for widget in self.widgets:
            widget.hide()

    def confirm(self):
        pass
