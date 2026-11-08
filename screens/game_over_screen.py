# Game Over Screen for the game, displaying the winner and a main menu button.
import pygame
import constants
from screens.base_screen import Screen


class GameOverScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)

        self.window_width = window_width
        self.window_height = window_height

        # The winning player will be provided by PlayingScreen
        self.winner = None

        self.title_font = pygame.font.SysFont(
            constants.FONT_STYLE, 64
        )

        self.winner_font = pygame.font.SysFont(
            constants.FONT_STYLE, 40
        )

        self.button_font = pygame.font.SysFont(
            constants.FONT_STYLE, 28
        )

        # Main menu button
        self.menu_button = pygame.Rect(
            window_width // 2 - 130,
            window_height // 2 + 110,
            260,
            60
        )

    def set_winner(self, winner):
        # Save the winning Player object
        self.winner = winner

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.menu_button.collidepoint(event.pos):
                    self.manager.change_screen("menu")

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.manager.change_screen("menu")

    def draw(self, surface):
        surface.fill(constants.BACKGROUND_COLOR)
        title_text = self.title_font.render(
            "GAME OVER",
            True,
            constants.TEXT_COLOR
        )

        title_rect = title_text.get_rect(
            center=(self.window_width // 2, 180)
        )

        surface.blit(title_text, title_rect)

        # Display the winning player
        if self.winner is not None:

            if self.winner.is_bot:
                result = "BOT VICTORY"
            else:
                result = "PLAYER VICTORY"

            result_text = self.winner_font.render(
                result,
                True,
                constants.TEXT_COLOR
            )

            result_rect = result_text.get_rect(
                center=(self.window_width // 2, 280)
            )

            surface.blit(result_text, result_rect)

            winner_text = self.winner_font.render(
                f"{self.winner.name} Wins!",
                True,
                self.winner.color
            )

            winner_rect = winner_text.get_rect(
                center=(self.window_width // 2, 340)
            )

            surface.blit(winner_text, winner_rect)

        # Fancy highlight of button
        mouse_position = pygame.mouse.get_pos()

        if self.menu_button.collidepoint(mouse_position):
            button_color = constants.BUTTON_HOVER_COLOR
        else:
            button_color = constants.BUTTON_COLOR

        pygame.draw.rect(
            surface,
            button_color,
            self.menu_button,
            border_radius=8
        )

        # Main menu button text
        button_text = self.button_font.render(
            "Main Menu",
            True,
            constants.WHITE
        )

        button_rect = button_text.get_rect(
            center=self.menu_button.center
        )

        surface.blit(button_text, button_rect)