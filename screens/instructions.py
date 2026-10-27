# Instructions Screen
from ui.instructions_menu import InstructionsMenu
from Screens.base_screen import Screen

class InstructionScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)
        self.instruction_menu = InstructionsMenu(screen=manager.screen, on_exit=manager.go_back)

        self.widgets = [self.instruction_menu.buttons]

    def handle_event(self, event):
        pass

    def draw(self, surface):
        self.instruction_menu.draw(surface)

    def update(self):
        pass