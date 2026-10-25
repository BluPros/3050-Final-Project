## IMPORT SYS PATH TO PARENT FOLDER ALLOWS RUN
## MUST BE ABOVE import ui.instructions_menu
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui.instructions_menu import InstructionsMenu
import constants
import pygame
import pygame_widgets
from pygame_widgets.button import Button


pygame.init()

win = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Risk - Main Menu")

clock = pygame.time.Clock()
running = True
show_instructions = False

def close():
    global show_instructions
    show_instructions = False
    instructions.buttons.hide()
    open_button.show()

instructions = InstructionsMenu(screen=win, on_exit=close)

def open_instructions():
    global show_instructions
    show_instructions = True
    open_button.hide()
    instructions.buttons.show()

open_button = Button(
    win,
    490, 300, 300, 70,
    text="Instructions",
    fontSize=30,
    inactiveColour=(139, 99, 62),
    hoverColour=(169, 135, 91),
    pressedColour=(73, 50, 31),
    onClick=open_instructions
)

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if show_instructions:
        instructions.draw(win)
    else:
        win.fill((35, 90, 45))

    pygame_widgets.update(events)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
