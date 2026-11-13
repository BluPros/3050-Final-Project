import random

import pygame

from pygame_widgets.button import Button

from constants import (
    PLAYER_COLORS,
    BOT_ICON_COLOR,
    TEXT_COLOR,
    ICON_WIDTH,
    ICON_HEIGHT
)

BOT_NAMES = [
    "Colonel Mustard",
    "General Chaos",
    "Lord Farquad",
    "Staff Duty",
    "King Pin",
    "Queen Elizabeth"
]

class BotIcon:
    """Represents the icon for a bot in the game, including color selection and name display."""
    def __init__(self, surface, existing_names):
        self.surface = surface
        self.x_center = 0
        self.y_center = 400
        self.color_index = 0
        self.player_color = PLAYER_COLORS[self.color_index]
        self.difficulties = ["easy", "medium", "hard"]
        self.difficulty_index = 0
        self.difficulty = self.difficulties[self.difficulty_index]
        self.left_color_button, self.right_color_button = self.create_color_buttons()
        self.name = self.generate_name(existing_names)
        self.difficulty_button = self.create_difficulty_button()
        self.update_attributes()

    @staticmethod
    def generate_name(existing_names):
        if existing_names is None:
            existing_names = []

        available_names = [
            name for name in BOT_NAMES
            if name not in existing_names
        ]

        if available_names:
            return random.choice(available_names)

    def update_attributes(self):
        # Update button positions
        self.left_color_button.setX(self.x_center - 73)
        self.left_color_button.setY(self.y_center - 10)
        self.right_color_button.setX(self.x_center + 53)
        self.right_color_button.setY(self.y_center - 10)
        self.difficulty_button.setX(self.x_center - 50)
        self.difficulty_button.setY(self.y_center + 76)

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

    def create_difficulty_button(self):
        """Create the button used to change bot difficulty."""
        return Button(
            self.surface,
            0, 0, 100, 20,
            text=self.difficulty.capitalize(),
            fontSize=13,
            inactiveColour=(139, 99, 62),
            hoverColour=(169, 135, 91),
            pressedColour=(73, 50, 31),
            onClick=self.change_difficulty
        )

    def change_difficulty(self):
        """Cycle between Easy, Medium, and Hard."""
        self.difficulty_index = (
            self.difficulty_index + 1
        ) % len(self.difficulties)

        self.difficulty = self.difficulties[self.difficulty_index]

        self.difficulty_button.setText(
            self.difficulty.capitalize()
        )

    def draw(self, surface):
        # Background box
        bg_rect = pygame.Rect(self.x_center-95, self.y_center-95, ICON_WIDTH, ICON_HEIGHT)
        pygame.draw.rect(surface, BOT_ICON_COLOR, bg_rect)

        # Text Identifying if it's a player or bot
        font = pygame.font.SysFont("georgia", 18)
        text_surface = font.render("Bot", True, TEXT_COLOR)
        text_x = self.x_center
        text_y = self.y_center - 70
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)
        # Text displaying bot's name
        font = pygame.font.SysFont("georgia", 16)
        text_surface = font.render(self.name, True, TEXT_COLOR)
        text_x = self.x_center
        text_y = self.y_center + 55
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)
        # Color selection box
        color_box_x = self.x_center - 33
        color_box_y = self.y_center - 33
        color_box = pygame.Rect(color_box_x, color_box_y, 66, 66)
        pygame.draw.rect(surface, self.player_color, color_box)
