from ui.phases.panel import PhasePanel
import pygame
from constants import TEXT_COLOR, FONT_STYLE, CLAIM_COLOR

class ClaimPanel(PhasePanel):
    def __init__(self, surface, on_close=None):
        super().__init__(surface, on_close=on_close)
        self.title = "Claim Territory"
        self.message = "PLAYER WHOEVER, PLEASE SELECT THE TERRITORY YOU WISH TO CLAIM"

    def show(self, message):
        super().show(message)

    def hide(self):
        super().hide()

    def draw(self):
        if self.visible:
            super().draw(background_color=CLAIM_COLOR)
            # Draw message
            font = pygame.font.SysFont(FONT_STYLE, 20)
            lines = self.message.split("\n")

            for index, line in enumerate(lines):
                text = font.render(line, True, TEXT_COLOR)
                text_rect = text.get_rect(center=(self.x_center, self.y_center))
                self.surface.blit(text, text_rect)