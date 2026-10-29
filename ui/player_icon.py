import constants
import pygame
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from constants import *

class PlayerIcon:
    def __init__(self, surface):
        self.surface = surface
        self.x_center = 0
        self.y_center = 400
        self.color_index = 0
        self.player_color = PLAYER_COLORS[self.color_index]
        self.left_color_button, self.right_color_button = self.create_color_buttons()
        self.name_input = self.create_name_input()
        self.update_attributes()

    def update_attributes(self):
        # Update button positions
        self.left_color_button.setX(self.x_center - 73)
        self.left_color_button.setY(self.y_center - 10)
        self.right_color_button.setX(self.x_center + 53)
        self.right_color_button.setY(self.y_center - 10)
        # Update name_input box position
        self.name_input.setX(self.x_center - 85)
        self.name_input.setY(self.y_center + 55)

    def create_color_buttons(self):
        left_button = Button(
            self.surface,
            0, 0, 20, 20,
            inactiveColour=(139, 99, 62),
            hoverColour=(169, 135, 91),
            pressedColour=(73, 50, 31),
            onClick=self.change_color_left
        )
        right_button = Button(
            self.surface,
            0, 0, 20, 20,
            inactiveColour=(139, 99, 62),
            hoverColour=(169, 135, 91),
            pressedColour=(73, 50, 31),
            onClick=self.change_color_right
        )

        return left_button, right_button

    def change_color_left(self):
        if self.color_index == 0:
            self.color_index = 5
        else:
            self.color_index -= 1
        self.player_color = PLAYER_COLORS[self.color_index]


    def change_color_right(self):
        if self.color_index == 5:
            self.color_index = 0
        else:
            self.color_index += 1
        self.player_color = PLAYER_COLORS[self.color_index]

    def create_name_input(self):
        name_input = TextBox(
            self.surface,
            0, 0, 170, 28,
            isSubWidget=False,
            colour = WHITE,
            textColour=BLACK,
            font=pygame.font.SysFont("georgia", 12),
            onTextChanged=self.validate_text,
            fontSize=16,
            placeholderText="Enter Name",
            placeholderColor=GRAY
        )
        return name_input

    def validate_text(self):
        text = self.name_input.getText()
        if len(text) > 20:
            self.name_input.setText(text[:20])

    def draw(self, surface):
        # Background box
        bg_rect = pygame.Rect(self.x_center-95, self.y_center-95, ICON_WIDTH, ICON_HEIGHT)

        # Text Identifying if it's a player or bot
        font = pygame.font.SysFont("georgia", 18)
        text_surface = font.render("Player", True, TEXT_COLOR)
        text_x = self.x_center
        text_y = self.y_center - 70
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)

        # Color selection box
        color_box_x = self.x_center - 33
        color_box_y = self.y_center - 33
        color_box = pygame.Rect(color_box_x, color_box_y, 66, 66)

        # Images for left and right arrows

        # Drawing everything
        pygame.draw.rect(surface, PLAYER_ICON_COLOR, bg_rect)
        pygame.draw.rect(surface, self.player_color, color_box)
        # Got to add the images still
        surface.blit(text_surface, text_rect)