import pygame
import constants

class PhasePanel:
    def __init__(self, surface, on_close=None):
        self.surface = surface
        self.x_center = constants.PANEL_X_CENTER
        self.y_center = constants.PANEL_Y_CENTER
        self.x_left = constants.PANEL_X_LEFT
        self.y_top = constants.PANEL_Y_TOP
        self.height = constants.PANEL_HEIGHT
        self.width = constants.PANEL_WIDTH
        self.message = "Test"
        self.visible = False
        self.current_player = None
        self.background_rect = pygame.Rect(
            self.x_left, self.y_top, self.width, self.height
        )
        self.on_close = on_close

    def show(self, message):
        self.message = message
        self.visible = True

    def hide(self):
        self.visible = False
        self.message = ""

        if self.on_close:
            self.on_close()

    def set_current_player(self, current_player):
        self.current_player = current_player

    def draw(self, background_color):
        # Draw phase panel
        pygame.draw.rect(
            self.surface, background_color, self.background_rect
        )

        # Draw title
        font = pygame.font.SysFont(constants.FONT_STYLE, 30)
        text = font.render(self.title, True, constants.TEXT_COLOR)
        text_rect = text.get_rect(
            center=(self.x_left + self.width // 2,
                    self.y_top + 30)
        )
        self.surface.blit(text, text_rect)
