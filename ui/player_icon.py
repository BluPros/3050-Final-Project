import constants
import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from constants import *

class PlayerIcon:
    def __init__(self, type_of_player, surface):
        self.x_pos = 0
        self.y_pos = 0
        self.title_text = type_of_player
        self.left_color_button, self.right_color_button = self.create_color_buttons()
        self.color_index = 0
        self.player_color = PLAYER_COLORS[self.color_index]
        self.name_input = self.create_name_input()
        self.surface = surface

    def update_attributes(self, x_position, y_position):
        self.x_pos = x_position
        self.y_pos = y_position
        # Update button positions
        self.left_color_button.x = self.x_pos + 21
        self.left_color_button.y = self.y_pos + ICON_HEIGHT // 2
        self.right_color_button.x = self.x_pos + 139
        self.right_color_button.y = self.y_pos + ICON_HEIGHT // 2
        # Update name_input box position
        self.name_input.x = self.x_pos + ICON_WIDTH // 2
        self.name_input.y = self.y_pos + 150

    def create_color_buttons(self):
        left_button = Button(
            self.surface,
            0, 0, 20, 20,
            inactiveColour=(139, 99, 62),
            hoverColour=(169, 135, 91),
            pressedColour=(73, 50, 31),
            onClick=self.change_color_left(self)
        )
        right_button = Button(
            self.surface,
            0, 0, 20, 20,
            inactiveColour=(139, 99, 62),
            hoverColour=(169, 135, 91),
            pressedColour=(73, 50, 31),
            onClick=self.change_color_right(self)
        )

        return left_button, right_button

    def change_color_left(self):
        if self.color_index == 0:
            self.color_index = 6
        else:
            self.color_index -= 1
        self.player_color = PLAYER_COLORS[self.color_index]


    def change_color_right(self):
        if self.color_index == 6:
            self.color_index = 0
        else:
            self.color_index += 1
        self.player_color = PLAYER_COLORS[self.color_index]

    def create_name_input(self):
        name_input = TextBox(
            self.surface,
            0, 0, 170, 20,
            isSubWidget=False,
            colour = WHITE,
            textColour=BLACK,
            onTextChanged=self.validate_text(self.name_input.getText()),
            font="georgia",
            fontSize=12
        )
        return name_input

    def validate_text(self, text):
        if len(text) > 20:
            self.name_input.setText(text[0:20])

    def draw(self, surface):
        # Background box
        bg_rect = pygame.Rect(self.x_pos, self.y_pos, ICON_WIDTH, ICON_HEIGHT)

        # Text Identifying if it's a player or bot
        font = pygame.font.SysFont("georgia", 18)
        text_surface = font.render(self.title_text, True, TEXT_COLOR)
        text_x = self.x_pos + ICON_WIDTH // 2
        text_y = self.y_pos + 10
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)

        # Color selection box
        color_box_x = self.x_pos + ICON_WIDTH // 2 - 33
        color_box_y = self.y_pos + ICON_HEIGHT // 2 - 33
        color_box = pygame.Rect(color_box_x, color_box_y, 66, 66)

        # Images for left and right arrows

        # Drawing everything
        pygame.draw.rect(surface, ICON_COLOR, bg_rect)
        pygame.draw.rect(surface, self.player_color, color_box)
        # Gotta add the images still
        surface.blit(text_surface, text_rect)