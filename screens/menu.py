import pygame
from constants import WHITE, LIGHT_BLUE
from pygame_widgets.button import Button
from screens.base_screen import Screen

# Menu Screen
# TODO: add title/background

class MenuScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)
        # Button Vars
        button_width = 200
        button_height = 60
        self.center_x = center_x = (window_width - button_width) // 2
        self.center_y = center_y = (window_height - button_height) // 2

        # store buttons in self.widgets which hides and shows automatically
        self.widgets = [
            Button(manager.screen, center_x - button_width, center_y + 100, button_width, button_height, 
            text="Play", onClick=lambda: manager.change_screen("playing"), 
            inactiveColour=LIGHT_BLUE, pressedColour=WHITE),
            Button(manager.screen, center_x + button_width, center_y + 100, button_width, button_height, 
            text="Quit", onClick=manager.quit_game, 
            inactiveColour=LIGHT_BLUE, pressedColour=WHITE),
            Button(manager.screen, center_x, center_y + 100, button_width, button_height, 
            text="Help", onClick=lambda: manager.change_screen("instructions"), 
            inactiveColour=LIGHT_BLUE, pressedColour=WHITE)
        ]

    def handle_event(self, event):
        pass # pygame_widgets handle button clicks

    def draw(self, surface):
        # pygame_widgets draw the buttosn, draw title/background here
        ## Title
        font = pygame.font.SysFont(None, 52)
        text_surface = font.render("Risk! Global Domination.", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.center_x, self.center_y)
        surface.blit(text_surface, text_rect)

        ## Background


    def update(self):
        pass
