from pygame_widgets.button import Button
import pygame
import constants
from ui.phases.panel import PhasePanel
from constants import DEPLOY_COLOR, FONT_STYLE, TEXT_COLOR

class DeployPanel(PhasePanel):
    def __init__(self, surface, on_close=None):
        super().__init__(surface, on_close=on_close)
        self.title = "Deploy"
        self.message = "PLAYER WHOEVER, PLEASE DEPLOY YOUR TROOPS"

        self.current_troop_count = 0

        self.cancel_button = Button(
            surface,
            self.x_left + 45, self.y_top + self.height - 45,
            160, 40,
            text="Cancel",
            onClick=self.cancel,
            inactiveColour=constants.BUTTON_COLOR,
            pressedColour=constants.WHITE,
            hoverColour=constants.BUTTON_HOVER_COLOR
        )

        self.confirm_button = Button(
            surface,
            self.x_left + 255, self.y_top + self.height - 45,
            160, 40,
            text="Confirm",
            onClick=self.confirm_deployment,
            inactiveColour=constants.BUTTON_COLOR,
            pressedColour=constants.WHITE,
            hoverColour=constants.BUTTON_HOVER_COLOR
        )

        self.cancel_button.hide()
        self.confirm_button.hide()


    def show(self, message):
        super().show(message)
        self.cancel_button.show()
        self.confirm_button.show()

    def hide(self):
        super().hide()
        self.cancel_button.hide()
        self.confirm_button.hide()

    # TODO: Have to implement cancel deployment logic
    def cancel(self):
        pass
    # TODO: Have to implement confirm deployment logic
    def confirm_deployment(self):
        pass

    def update_troop_count(self, troop_count):
        self.current_troop_count = troop_count

    def draw(self):
        if self.visible:
            super().draw(background_color=DEPLOY_COLOR)
            # Drawing Instructions
            font = pygame.font.SysFont(FONT_STYLE, 20)
            text = font.render(f"{self.current_player.player_name}", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(self.x_center, self.y_center))
            self.surface.blit(text, text_rect)
