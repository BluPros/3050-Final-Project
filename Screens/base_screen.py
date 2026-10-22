# Make a Screen base class to ensure the interface required for GameStateManager
# is explicit

class Screen:
    def __init__(self, manager):
        self.manager = manager
        self.widgets = []

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

    def on_exit(self):
        for widget in self.widgets:
            widget.hide()

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass

    def update(self):
        pass