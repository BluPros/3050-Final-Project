import pygame
from constants import WHITE, BACKGROUND_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR
from pygame_widgets.button import Button
from Screens.base_screen import Screen

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
            Button(manager.screen, center_x - 1.5 * button_width, center_y + 100, button_width, button_height,
                   text="New Game", onClick=lambda: manager.change_screen("new_game"),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x - 0.5 * button_width, center_y + 100, button_width, button_height,
                   text = "Load Game", onClick=lambda: manager.change_screen("load_game"),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x + 0.5 * button_width, center_y + 100, button_width, button_height,
                   text="Quit", onClick=manager.quit_game,
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x + 1.5 * button_width, center_y + 100, button_width, button_height,
                   text="Help", onClick=lambda: manager.change_screen("instructions"),
                   inactiveColour=BUTTON_COLOR, pressedColour=WHITE, hoverColour=BUTTON_HOVER_COLOR),
        ]

    def handle_event(self, event):
        pass # pygame_widgets handle button clicks

    def draw(self, surface):
        # pygame_widgets draw the buttons, draw title/background here
        ## Title
        surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("georgia", 52)
        text_surface = font.render("Risk! Global Domination.", True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.center_x, self.center_y)
        surface.blit(text_surface, text_rect)

        ## Background


    def update(self):
        pass
