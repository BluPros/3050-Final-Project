import pygame
from constants import (
    CARD_WIDTH,
    CARD_Y_CENTER,
    CARD_HEIGHT,
    TEXT_COLOR
)

class PlayerCard:
    """Displays the player stats during gameplay"""
    def __init__(self, surface, player):
        self.surface = surface
        self.x_center = 0
        self.y_center = CARD_Y_CENTER
        self.player_color = player.player_color
        self.name = player.name
        self.territory_count = player.territory_count
        self.troop_count = player.troop_count
        self.card_count = player.card_count

    def draw(self, surface):
        # Draw Background Rectangle
        bg_rect = pygame.Rect(
            self.x_center-CARD_WIDTH//2,
            self.y_center-CARD_HEIGHT//2,
            CARD_WIDTH,
            CARD_HEIGHT
        )
        pygame.draw.rect(surface, self.player_color, bg_rect)
        # Write the player name to the screen
        font = pygame.font.SysFont("georgia", 12)
        text_surface = font.render(self.name, True, TEXT_COLOR)
        text_x = self.x_center
        text_y = self.y_center - 3*CARD_HEIGHT//8
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)
        # Write the player Troop Count to the screen
        text_surface = font.render(f"Troop Count: {self.troop_count}", True, TEXT_COLOR)
        text_y = self.y_center - CARD_HEIGHT//8
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)
        # Write the Territory Count to the screen
        text_surface = font.render(f"Terr. Count: {self.territory_count}", True, TEXT_COLOR)
        text_y = self.y_center + CARD_HEIGHT//8
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)
        # Write the Card Count to the screen
        text_surface = font.render(f"Card Count: {self.card_count}", True, TEXT_COLOR)
        text_y = self.y_center + CARD_HEIGHT//8
        text_rect = text_surface.get_rect()
        text_rect.center = (text_x, text_y)
        surface.blit(text_surface, text_rect)

    def set_x_center(self, x_center):
        self.x_center = x_center

    def set_troop_count(self, troop_count):
        self.troop_count = troop_count

    def set_territory_count(self, territory_count):
        self.territory_count = territory_count

    def set_card_count(self, card_count):
        self.card_count = card_count
