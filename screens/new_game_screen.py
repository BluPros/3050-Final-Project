# New Game Screen
from ui.new_game_menu import NewGameMenu
from Screens.base_screen import Screen

class NewGameScreen(Screen):
    def __init__(self, manager, window_width, window_height):
        super().__init__(manager)
        self.new_game_menu = NewGameMenu(screen=manager.screen, on_exit=manager.go_back)

        self.widgets = self.new_game_menu.widgets

    def handle_event(self, event):
        pass

    def draw(self, surface):
        self.new_game_menu.draw(surface)

    def update(self):
        pass

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

        for icon in self.new_game_menu.players + self.new_game_menu.bots:
            icon.left_color_button.show()
            icon.right_color_button.show()

        for player in self.new_game_menu.players:
            player.name_input.show()
