import pygame
from constants import *

class PopUp:
    def __init__(self, surface, message="", on_close=None):
        self.surface = surface
        self.message = message
        self.visible = False
        self.on_close = on_close
        self.title = ""
        self.width = 960
        self.height = 560
        self.x = 160
        self.y = 80

        self.background_rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

    def show(self, message):
        self.message = message
        self.visible = True

    def hide(self):
        self.visible = False
        self.message = ""

        if self.on_close:
            self.on_close()

    def draw(self):
        if not self.visible:
            return

        # Draw a translucent overlay over the existing screen
        overlay = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 120))
        self.surface.blit(overlay, (0, 0))

        # Draw popup panel
        pygame.draw.rect(
            self.surface, BACKGROUND_COLOR, self.background_rect
        )
        pygame.draw.rect(
            self.surface, BUTTON_COLOR, self.background_rect, 4
        )

        # Draw title
        font = pygame.font.SysFont("georgia", 52)
        text = font.render(self.title, True, TEXT_COLOR)
        text_rect = text.get_rect(
            center=(self.x + self.width//2,
                    self.y + 60)
        )
        self.surface.blit(text, text_rect)
        # Draw message
        font = pygame.font.SysFont("georgia", 20)
        lines = self.message.split("\n")

        for index, line in enumerate(lines):
            text = font.render(line, True, TEXT_COLOR)
            text_rect = text.get_rect(
                center=(
                    self.x + self.width // 2,
                    self.y + 100 + index * 30
                )
            )
            self.surface.blit(text, text_rect)