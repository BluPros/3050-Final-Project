"""Child of base screen, displays menu and navigable buttons"""
import pygame
from pygame_widgets.button import Button
import constants
from screens.base_screen import Screen

# Menu Screen

class MenuScreen(Screen):
    """Child of base_screen, uses same defined behavior to build basic
    menu and buttons for gameplay, navigation, help, quit"""
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)
        # Button Vars
        button_width = 200
        button_height = 60
        self.center_x = center_x = (window_width - button_width) // 2
        self.center_y = center_y = (window_height - button_height) // 2

        # store buttons in self.widgets which hides and shows automatically
        self.widgets = [
            Button(manager.screen, center_x - 1.5 * button_width, center_y + 100,
                   button_width, button_height,
                   text="New Game", onClick=lambda: manager.change_screen("new_game"),
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x - 0.5 * button_width, center_y + 100,
                   button_width, button_height,
                   text="Continue", onClick=manager.resume_or_new_game,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x + 0.5 * button_width, center_y + 100,
                   button_width, button_height,
                   text="Quit", onClick=manager.quit_game,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            Button(manager.screen, center_x + 1.5 * button_width, center_y + 100,
                   button_width, button_height,
                   text="Help", onClick=lambda: manager.change_screen("instructions"),
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
        ]

    def handle_event(self, event):
        """Inherited from base, potentially utilized for later events,
        maybe not because it is just a menu pygame_widgets handle button clicks"""

    def draw(self, surface):
        """Once again, inherited and called in manager to draw elements"""
        # pygame_widgets draw the buttons, draw title/background here
        ## Title
        surface.fill(constants.BACKGROUND_COLOR)
        font = pygame.font.SysFont(constants.FONT_STYLE, 52)
        text_surface = font.render("Risk! Global Domination.", True, constants.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.center_x, self.center_y)
        surface.blit(text_surface, text_rect)

        ## Background


    def update(self):
        pass
