"""
This class is intended to be...
"""
import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray
from GLOBALS import WINDOW_WIDTH, WINDOW_HEIGHT, INSTRUCTIONS

class InstructionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = self.create_buttons()
        self.current_instruction = "setup"
        self.message = INSTRUCTIONS[self.current_instruction]
        self.running = True
        self.font = self.create_font()
        self.text = self.font.render(self.current_instruction, True, (255, 255, 255))

    def create_buttons(self):
        buttons = ButtonArray(
        win=self.screen,
        x=0,
        y=0,
        width=WINDOW_WIDTH,
        height = WINDOW_HEIGHT/10,
        shape = (5,1),
        border = 0,
        texts = ('Setup','Deploy','Attack','Fortify', 'Exit'),
        onClicks = (lambda: self.change_tab("setup"),
                    lambda: self.change_tab("deploy"),
                    lambda: self.change_tab("attack"),
                    lambda: self.change_tab("fortify"),
                    lambda: self.close_instructions()
                    )
        )
        return buttons

    def create_font(self):
        font = pygame.font.SysFont("gillsans", 20)
        return font

    def update_text(self, text):
        self.screen.fill((0, 0, 0))
        self.screen.blit(text,
                        (5, WINDOW_HEIGHT/10 + 5)
                         )

    def close_instructions(self):
        # Close the window (clear screen and redraw the Playing screen)
        self.running = False
        # Switch game state back to "Playing"
        pass

    def change_tab(self, tab):
        self.current_instruction = tab
        self.message = INSTRUCTIONS[self.current_instruction]
        self.text = self.font.render(self.message, True, (255,255,255))
        self.update_text(self.text)
        print(tab)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    quit()

            pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
            pygame.display.update()
