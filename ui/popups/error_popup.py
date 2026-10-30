from pygame_widgets.button import Button
from ui.popups.popup import PopUp
from constants import BUTTON_COLOR, WHITE, BUTTON_HOVER_COLOR

class ErrorPopUp(PopUp):
    def __init__(self, surface, on_close=None):
        super().__init__(surface, on_close=on_close)

        self.title = "Error"

        self.back_button = Button(
            surface,
            560, 540,
            160, 40,
            text="Back",
            onClick=self.hide,
            inactiveColour=BUTTON_COLOR,
            pressedColour=WHITE,
            hoverColour=BUTTON_HOVER_COLOR
        )

        self.back_button.hide()

    def show(self, message):
        super().show(message)
        self.back_button.show()

    def hide(self):
        super().hide()
        self.back_button.hide()

    def draw(self):
        if self.visible:
            super().draw()