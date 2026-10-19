import pygame

# File will include a library of pre-built elements to incorporate in various menus and UI screens


class Button:
    def __init__(self, text, x, y, width, height, action, color, hover_color=None, text_color=(0, 0, 0), font_size=32):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.color = color
        self.hover_color = hover_color if hover_color is not None else color
        self.text_color = text_color
        # None = pygame's default font
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(
            mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()
