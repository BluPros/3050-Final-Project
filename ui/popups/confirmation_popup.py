from pygame_widgets.button import Button
from ui.popups.popup import PopUp
from constants import BUTTON_COLOR, WHITE, BUTTON_HOVER_COLOR

class ConfirmationPopUp(PopUp):
    def __init__(self, surface, on_close=None):
        super().__init__(surface, on_close=on_close)

        self.on_confirm = None

        self.title = "Confirmation"

        self.back_button = Button(
            surface,
            400, 540,
            160, 40,
            text="Back",
            onClick=self.hide,
            inactiveColour=BUTTON_COLOR,
            pressedColour=WHITE,
            hoverColour=BUTTON_HOVER_COLOR
        )

        self.confirm_button = Button(
            surface,
            720, 540,
            160, 40,
            text="Confirm",
            onClick=self.confirm,
            inactiveColour=BUTTON_COLOR,
            pressedColour=WHITE,
            hoverColour=BUTTON_HOVER_COLOR
        )

        self.back_button.hide()
        self.confirm_button.hide()

    def show(self, message, on_confirm):
        super().show(message)
        self.on_confirm = on_confirm

        self.back_button.show()
        self.confirm_button.show()

    def hide(self):
        super().hide()
        self.back_button.hide()
        self.confirm_button.hide()
        self.on_confirm = None

    def confirm(self):
        if self.on_confirm:
            callback = self.on_confirm
            self.hide()
            callback()

    def draw(self):
        if self.visible:
            super().draw()