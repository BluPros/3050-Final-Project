"""
This class is intended to be...
"""
import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray
from data.instructions import INSTRUCTIONS
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR


class InstructionsMenu:
    def __init__(self, screen, on_exit):
        self.screen = screen
        ## on_exit is a lambda function passed in through init
        ## should call the change menu on the last screen we were on
        self.on_exit = on_exit
        self.current_instruction = "setup"
        self.message = INSTRUCTIONS[self.current_instruction]
        self.running = False
        self.visible = False
        self.font = self.create_font()
        self.buttons = self.create_buttons()
        self.buttons.hide()

    def create_buttons(self):
        buttons = ButtonArray(
            win=self.screen,
            x=0,
            y=0,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT//10,
            shape=(8, 1),
            border=2,
            texts=('Setup', 'Turn Order', 'Deploy', 'Attack',
                   'Risk Cards', 'Fortify', 'Winning', 'Exit'),
            colour=(0, 0, 0),
            fontColour=(232, 211, 165),
            onClicks=(lambda: self.change_tab("setup"),
                      lambda: self.change_tab("turn_order"),
                      lambda: self.change_tab("deploy"),
                      lambda: self.change_tab("attack"),
                      lambda: self.change_tab("risk_cards"),
                      lambda: self.change_tab("fortify"),
                      lambda: self.change_tab("winning"),
                      lambda: self.on_exit()
                      )
        )
        for button in buttons.buttons:
            button.colour = BUTTON_COLOR
            button.inactiveColour = (139, 99, 62)
            button.hoverColour = BUTTON_HOVER_COLOR
            button.pressedColour = (73, 50, 31)
            button.textColour = (232, 211, 165)
        return buttons

    def create_font(self):
        font = pygame.font.SysFont("georgia", 18)
        return font

    def update_text(self, message):
        y = WINDOW_HEIGHT // 10 + 5
        # Covert text into list of lines (split on \n)
        split_text = message.splitlines()
        for line in split_text:
            text = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (5, y))
            y += self.font.get_linesize()

    # Should be useless after conversion
    # def close_instructions(self):
    #     self.running = False
    #     self.visible = False

    def change_tab(self, tab):
        self.current_instruction = tab
        self.message = INSTRUCTIONS[self.current_instruction]

    # Should be useless after conversion
    # def run(self):
    #     # Reset the menu each time it is opened.
    #     self.running = True
    #     self.visible = True

    #     while self.running:
    #         events = pygame.event.get()

    #         for event in events:
    #             if event.type == pygame.QUIT:
    #                 self.close_instructions()
    #                 return "quit"

    #         self.screen.fill(BACKGROUND_COLOR)
    #         self.update_text(self.message)

    #         pygame_widgets.update(events)
    #         pygame.display.flip()

    #     return "closed"

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.update_text(self.message)
