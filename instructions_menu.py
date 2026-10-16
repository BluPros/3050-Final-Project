"""
This class is intended to be...
"""
import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray
from GLOBALS import WINDOW_WIDTH, WINDOW_HEIGHT, INSTRUCTIONS, BACKGROUND_COLOR, TEXT_COLOR

class InstructionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR)
        self.buttons = self.create_buttons()
        self.current_instruction = "setup"
        self.message = INSTRUCTIONS[self.current_instruction]
        self.running = True
        self.font = self.create_font()
        self.text = self.font.render(self.message, True, TEXT_COLOR)
        self.screen.blit(self.text,
                         (5, WINDOW_HEIGHT // 10 + 5)
                         )

    def create_buttons(self):
        buttons = ButtonArray(
        win=self.screen,
        x=0,
        y=0,
        width=WINDOW_WIDTH,
        height = WINDOW_HEIGHT//10,
        shape = (8,1),
        border = 2,
        texts = ('Setup','Turn Order','Deploy','Attack','Risk Cards','Fortify','Winning', 'Exit'),
        colour=(0,0,0),
        fontColour=(232, 211, 165),
        onClicks = (lambda: self.change_tab("setup"),
                    lambda: self.change_tab("turn_order"),
                    lambda: self.change_tab("deploy"),
                    lambda: self.change_tab("attack"),
                    lambda: self.change_tab("risk_cards"),
                    lambda: self.change_tab("fortify"),
                    lambda: self.change_tab("winning"),
                    lambda: self.close_instructions()
                    )
        )
        for button in buttons.buttons:
            button.colour = (139, 99, 62)
            button.inactiveColour = (139, 99, 62)
            button.hoverColour = (169, 135, 91)
            button.pressedColour = (73, 50, 31)
            button.textColour = (232, 211, 165)
        return buttons

    def create_font(self):
        font = pygame.font.SysFont("georgia", 18)
        return font

    def update_text(self, message):
        text = self.font.render(message, True, TEXT_COLOR)
        self.screen.blit(
            text,
            (5, WINDOW_HEIGHT // 10 + 5)
        )

    def close_instructions(self):
        # Close the window (clear screen and redraw the Playing screen)
        self.running = False
        # Switch game state back to "Playing"
        pass

    def change_tab(self, tab):
        self.current_instruction = tab
        self.message = INSTRUCTIONS[self.current_instruction]

    def run(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.screen.fill(BACKGROUND_COLOR)
            self.update_text(self.message)

            pygame_widgets.update(events)
            pygame.display.update()
