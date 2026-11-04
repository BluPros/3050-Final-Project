import pygame
from constants import *
from ui.player_icon import PlayerIcon
from ui.bot_icon import BotIcon
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
from pygame_widgets.button import Button

class NewGameMenu:
    def __init__(self, screen, on_exit):
        self.surface = screen
        ## on_exit is a lambda function passed in through init
        ## should call the change menu on the last screen we were on
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
        buttons = [
            # remove player button
            Button(self.surface, 220, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_player(),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # add Player Button
            Button(self.surface, 380, 220, 40, 40,
                   text="+", onClick=lambda: self.add_player(self.surface),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            # remove Bot Button
            Button(self.surface, 860, 220, 40, 40,
                   text="-", onClick=lambda: self.remove_bot(),
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

    def hide_widgets(self):
        for widget in self.widgets:
            widget.hide()

        for icon in self.players + self.bots:
            icon.left_color_button.hide()
            icon.right_color_button.hide()

        for player in self.players:
            player.name_input.hide()

    def show_widgets(self):
        for widget in self.widgets:
            widget.show()

        for icon in self.players + self.bots:
            icon.left_color_button.show()
            icon.right_color_button.show()

        for player in self.players:
            player.name_input.show()

    def show_error_popup(self, message):
        self.hide_widgets()
        self.error_popup.show(message)

    def show_confirmation_popup(self, message):
        self.hide_widgets()
        self.confirmation_popup.show(message, self.start_game)

    def add_player(self, surface):
        # Create new player and add to list
        if len(self.players) + len(self.bots) < 6 :
            player = PlayerIcon(surface)
            self.players.append(player)
        # Reset all player coordinates and draw them
        self.reconfigure_players()

    def remove_player(self):
        if self.players:
            deleted_player = self.players.pop()
            deleted_player.left_color_button.hide()
            deleted_player.right_color_button.hide()
            deleted_player.name_input.hide()
            self.reconfigure_players()

    def add_bot(self, surface):
        if len(self.players) + len(self.bots) < 6:
            existing_names = [
                                 icon.name for icon in self.bots
                             ] + [
                                 icon.name_input.getText()
                                 for icon in self.players
                                 if icon.name_input.getText().strip()
                             ]

            bot = BotIcon(surface, existing_names)
            self.bots.append(bot)

        self.reconfigure_players()

    def remove_bot(self):
        if self.bots:
            deleted_bot = self.bots.pop()

            deleted_bot.left_color_button.hide()
            deleted_bot.right_color_button.hide()

            self.reconfigure_players()

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
        for icon in self.players + self.bots:
            icon.draw(surface)
        # draw popups if needed and hide widgets
        self.error_popup.draw()
        self.confirmation_popup.draw()

    def confirm(self):
        confirmation_message = ""
        error_message = ""
        # Validating bot and player counts
        if not (len(self.players) + len(self.bots) >= 3 and len(self.players) > 0):
            error_message += (f"Invalid number of players.\nPlease ensure you have at least 3 total players, including "
                              f"bots. \nAt least one player has to be human.\nYou currently have {len(self.bots)}"
                              f" bot(s) and {len(self.players)} human player(s).\n")
        # Validating all player names
        for index, player in enumerate(self.players):
            if player.name_input.getText().strip() == "":
                error_message += f"Please enter a name for player {index + 1}.\n"
                
        # Validate player colors
        current_selected_colors = []
        for icon in self.players + self.bots:
            current_selected_colors.append(icon.player_color)
        if len(set(current_selected_colors)) != len(current_selected_colors):
            error_message += "Please ensure that all players have unique colors.\n"
        
        # If there are no errors, create confirmation message
        if error_message == "":
            confirmation_message += "Everything looks good! Your current players are:\n"
            for index, player in enumerate(self.players):
                confirmation_message += f"{index + 1}. {player.name_input.getText()}\n"

            if len(self.bots) > 0:
                confirmation_message += "Your current bots are:\n"
            for index, bot in enumerate(self.bots):
                confirmation_message += f"{index + 1}. {bot.name}\n"

        if error_message:
            self.show_error_popup(error_message)

        elif confirmation_message:
            self.show_confirmation_popup(confirmation_message)


    def back_to_main(self):
        for icon in self.players + self.bots:
            icon.right_color_button.hide()
            icon.left_color_button.hide()
        for player in self.players:
            player.name_input.hide()
        self.on_exit()

    def on_enter(self):
        for widget in self.widgets:
            widget.show()
        icons = self.players + self.bots
        for icon in icons:
            icon.right_color_button.show()
            icon.left_color_button.show()
        for player in self.players:
            player.name_input.show()

    def start_game(self):
        pass