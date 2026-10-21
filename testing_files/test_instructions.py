## IMPORT SYS PATH TO PARENT FOLDER ALLOWS RUN
## MUST BE ABOVE import instructions_menu
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import instructions_menu
import pygame
import pygame_widgets
from pygame_widgets.button import Button


pygame.init()

WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Risk - Main Menu")

clock = pygame.time.Clock()
running = True
show_instructions = False

instructions = instructions_menu.InstructionsMenu(screen=win)

open_button = Button(
    win,
    490, 300, 300, 70,
    text="Instructions",
    fontSize=30,
    inactiveColour=(139, 99, 62),
    hoverColour=(169, 135, 91),
    pressedColour=(73, 50, 31)
)

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if show_instructions:
        result = instructions.run()
        show_instructions = False

        if result == "quit":
            running = False

    else:
        win.fill((35, 90, 45))
        pygame_widgets.update(events)
        pygame.display.flip()

        if open_button.clicked:
            show_instructions = True

    clock.tick(60)

pygame.quit()
