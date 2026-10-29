import pygame
from constants import *
from ui.player_icon import PlayerIcon
from pygame_widgets.button import Button

class NewGameMenu:
    def __init__(self, screen, on_exit):
        self.surface = screen
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
            Button(self.surface, 220, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_player(self.surface),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Player Button
            Button(self.surface, 380, 220, 40, 40,
                   text="+", onClick=lambda: self.add_player(self.surface),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # remove Bot Button
            Button(self.surface, 860, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_bot(self.surface),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Bot Button
            Button(self.surface, 1020, 220, 40, 40,
                   text="+", onClick=lambda: self.add_bot(self.surface),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # Back Button
            Button(self.surface, 320, 640, 160, 60,
                   text="Back", onClick=lambda: self.back_to_main(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # Confirm Button
            Button(self.surface, 800, 640, 160, 60,
                   text="Confirm", onClick=lambda: self.confirm(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
        ]
        return buttons

    def add_player(self, surface):
        # Create new player and add to list
        if len(self.players) + len(self.bots) < 6 :
            player = PlayerIcon(surface)
            self.players.append(player)
        # Reset all player coordinates and draw them
        self.reconfigure_players()

    def remove_player(self, surface):
        if len(self.players) + len(self.bots) > 0 :
            deleted_player = self.players.pop()
            deleted_player.left_color_button.hide()
            deleted_player.right_color_button.hide()
            deleted_player.name_input.hide()
            self.reconfigure_players()

    def add_bot(self, surface):
        pass

    def remove_bot(self, surface):
        pass

    def reconfigure_players(self):
        icons = self.players + self.bots
        player_x_coordinates = ICON_X_POSITIONS.get(len(self.players) + len(self.bots), [])
        for icon, x in zip(icons, player_x_coordinates):
            icon.x_center = x
            icon.update_attributes()


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
        #redraw all icons
        for player in self.players:
            player.draw(surface)

    def hide_widgets(self):
        for widget in self.widgets:
            widget.hide()

    def confirm(self):
        pass

    def back_to_main(self):
        icons = self.players + self.bots
        for icon in icons:
            icon.right_color_button.hide()
            icon.left_color_button.hide()
            icon.name_input.hide()

        self.on_exit()

    def on_enter(self):
        for widget in self.widgets:
            widget.show()
        icons = self.players + self.bots
        for icon in icons:
            icon.right_color_button.show()
            icon.left_color_button.show()
            icon.name_input.show()