# New Game Screen
from ui.new_game_menu import NewGameMenu
from screens.base_screen import Screen

class NewGameScreen(Screen):
    """Represents the screen for starting a new game in the Risk game."""
    def __init__(self, manager, _window_width, _window_height):
        super().__init__(manager)
        self.new_game_menu = NewGameMenu(
            screen=manager.screen,
            on_exit=manager.go_back,
            on_start=manager.start_configured_game
        )

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

        for bot in self.new_game_menu.bots:
            bot.difficulty_button.show()

        for player in self.new_game_menu.players:
            player.name_input.show()

    def on_exit(self):
        super().on_exit()
        self.new_game_menu.hide_widgets()
