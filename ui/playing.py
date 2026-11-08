import pygame
from ui.popups.error_popup import ErrorPopUp
from ui.popups.confirmation_popup import ConfirmationPopUp
from pygame_widgets.button import Button
import constants

class PlayingOverlay:
    def __init__(self, screen, on_exit, game, on_end_phase=None, on_help=None):
        self.surface = screen
        self.on_exit = on_exit
        self.game = game
        self.on_end_phase = on_end_phase
        self.on_help = on_help
        self.players = []
        self.widgets = []
        self.deploy_widgets = []
        self.deploy_troop_counter = 0
        self.attack_widgets = []
        self.attack_troop_counter = 0
        self.fortify_widgets = []
        self.fortify_troop_counter = 0
        self.create_widgets()
        self.hide_widgets(self.widgets + self.deploy_widgets + self.attack_widgets + self.fortify_widgets)
        self.error_popup = ErrorPopUp(
            self.surface,
            on_close=self.show_widgets
        )
        self.confirmation_popup = ConfirmationPopUp(
            self.surface,
            on_close=self.show_widgets
        )


    # maintains clicked order for battle, move, fortify, etc.
    self.selected_src = None
    self.selected_dst = None
    # true after conquest, until confirms move-in
    self.moving_in = False
    # if owners are changing
    self.map_limbo = False

    def clear_selection(self):

        # Reset troop counters
        self.deploy_troop_counter = 0
        self.attack_troop_counter = 0
        self.fortify_troop_counter = 0

        self.selected_src = None
        self.selected_dst = None
        self.moving_in = False
        self.deploy_troop_counter = 0
        self.attack_troop_counter = 0
        self.fortify_troop_counter = 0


    def create_widgets(self):
        # Regular Buttons that show all the time.
        self.widgets =[
            # End Phase button
            Button(self.surface, 810, 440, constants.PANEL_WIDTH, 40,
                   text="End Phase", onClick=self.end_phase,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
                   
            # Help Menu Button
            Button(self.surface, 10, 10, 140, 40,
                   text="Help", onClick=self.show_help,
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),

            # Cards Menu Button
            Button(self.surface, 810, 510, 180, 147,
                   text="Cards", onClick=lambda: print("Cards button not implemented"), # Have to add real onClick Method
                   text="Help", onClick=lambda: print("printed help from playing screen"),
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]

        # Deployment Phase widgets
        self.deploy_widgets =[
            # Deploy Troops button
            Button(self.surface, 830, 386, constants.PANEL_WIDTH - 40, 40,
                   text="Deploy Troops", onClick=self.end_phase,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 316, 40, 40,
                   text="-", onClick=self.remove_deployment_troop,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 316, 40, 40,
                   text="+", onClick=self.add_deployment_troop,# TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]
        # Attack Phase widgets
        self.attack_widgets = [
            # Deploy Troops button
            Button(self.surface, 830, 390, constants.PANEL_WIDTH - 40, 40,
                   text="Initiate Attack", onClick=self.end_phase,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 340, 40, 40,
                   text="-", onClick=self.remove_attack_troop,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 340, 40, 40,
                   text="+", onClick=self.add_attack_troop,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]
        # Fortify Phase widgets
        self.fortify_widgets = [
            # Deploy Troops button
            Button(self.surface, 830, 390, constants.PANEL_WIDTH - 40, 40,
                   text="Move Troops", onClick=self.end_phase,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Remove troop button
            Button(self.surface, constants.PANEL_X_CENTER - 70, 340, 40, 40,
                   text="-", onClick=self.remove_fortify_troop,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR),
            # Add Troop button
            Button(self.surface, constants.PANEL_X_CENTER + 30, 340, 40, 40,
                   text="+", onClick=self.add_fortify_troop,
                   # TODO: placeholder onClick. Have to implement deploy button logic
                   inactiveColour=constants.BUTTON_COLOR, pressedColour=constants.WHITE,
                   hoverColour=constants.BUTTON_HOVER_COLOR)
        ]

    # Hides all the widgets we don't want to see
    def hide_widgets(self, widgets):
        for widget in widgets:
            widget.hide()

    # Optionally takes a list of widgets that we want to show.
    def show_widgets(self, widgets=None):
        if widgets is None:
            widgets = self.widgets

        for widget in widgets:
            widget.show()

    # Hide the widgets and show only the ones we need for this phase
    def update_phase_widgets(self):
        self.hide_widgets(
            self.deploy_widgets + self.attack_widgets + self.fortify_widgets
        )

        match self.game.phase:
            case "deploy":
                self.show_widgets(self.deploy_widgets)
            case "attack":
                self.show_widgets(self.attack_widgets)
            case "fortify":
                self.show_widgets(self.fortify_widgets)

    def select_territory(self, territory):
        player = self.game.current_player
        owned = territory.owner_id == player.player_id

        if self.game.phase == "deploy":
            if owned:
                self.selected_src = territory

        elif self.game.phase == "attack":
            if self.moving_in:
                return
            if owned and territory.troops >= 2:
                self.selected_src = territory
                self.selected_dst = None
                self.attack_troop_counter = min(3, territory.troops - 1)
            elif not owned and self.selected_src and self.selected_src.is_neighbor(territory.name):
                self.selected_dst = territory
        
        #TODO: not checking possible connection here but lowk fine, cause it happens either way
        # probably will need to print my error messages n' stuff somehow
        elif self.game.phase == "fortify":
            if not owned:
                return
            if territory is self.selected_src:
                self.clear_selection()
            elif self.selected_src is None:
                self.selected_src = territory
            else: self.selected_dst = territory

    def remove_deployment_troop(self):
        if self.deploy_troop_counter > 0:
            self.deploy_troop_counter -= 1

    def add_deployment_troop(self):
        player = self.game.current_player

        if player is None:
            return

        if self.deploy_troop_counter < player.reinforcements:
            self.deploy_troop_counter += 1

    def remove_attack_troop(self):
        if self.moving_in:
            minimum = self.game.pending_conquest["min_move"]
        else:
            minimum = 1

        if self.attack_troop_counter > minimum:
            self.attack_troop_counter -= 1


    def add_attack_troop(self):
        src = self.selected_src
        if src is None:
            return

        if self.moving_in:
            limit = src.troops -1
        else:
            limit = min(3, src.troops -1)

        if self.attack_troop_counter < limit:
            self.attack_troop_counter += 1

    def remove_fortify_troop(self):
        if self.fortify_troop_counter > 0:
            self.fortify_troop_counter -= 1

    def add_fortify_troop(self):
        territory = self.game.current_fortifying_territory
        if territory is None:
            return
        if self.fortify_troop_counter < territory.troops:
            self.fortify_troop_counter += 1

    def configure_player_cards(self, players):
        player_x_coordinates = constants.CARD_X_POSITIONS.get(len(players), [])
        for player, x in zip(players, player_x_coordinates):
            player.x_center = x

    def draw(self, surface):
        # Title
        font = pygame.font.SysFont(constants.FONT_STYLE, 30)
        text_surface = font.render("Playing Screen", True, constants.TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (640, 30)
        surface.blit(text_surface, text_rect)

    def draw_text(self, message, x, y, font_size, font_color=constants.TEXT_COLOR):
        # Make font object
        font = pygame.font.SysFont(constants.FONT_STYLE, font_size)
        # update the text
        text = font.render(message, True, font_color)
        # Write text to screen
        text_rect = text.get_rect(center=(x, y))
        self.surface.blit(text, text_rect)


    def draw_setup(self, player, step, hover_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.CLAIM_COLOR, background_rect, border_radius=8
        )
        # Selected territory box
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20 , constants.PANEL_Y_TOP + 240, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius = 8
        )
        # Title
        self.draw_text(
            message=f"{step} Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=40,
            font_color=constants.TEXT_COLOR
        )

        # Draw Player Name
        self.draw_text(
            message=player.name,
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 110,
            font_size=24,
            font_color=constants.TEXT_COLOR
        )

        # Draw Instructions
        if step == "Claim":
            self.draw_text(
                message="Select an unclaimed territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 170,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )

            # Draw Selected Territory if one has been selected
            if hover_territory:
                self.draw_text(
                    message="Click to Claim:",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 270,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
                self.draw_text(
                    message=hover_territory.name,
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 310,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
            else:
                self.draw_text(
                    message="No territory selected.",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 295,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
        elif step == "Reinforce":
            self.draw_text(
                message="Select a territory you want to reinforce.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 170,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )

            # Draw Selected Territory if one has been selected
            if hover_territory:
                self.draw_text(
                    message="Click to Reinforce:",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 270,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
                self.draw_text(
                    message=hover_territory.name,
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 310,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )
            else:
                self.draw_text(
                    message="No territory selected.",
                    x=constants.PANEL_X_CENTER,
                    y=constants.PANEL_Y_TOP + 295,
                    font_size=24,
                    font_color=constants.TEXT_COLOR
                )

    def draw_deploy(self, player, selected_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.DEPLOY_COLOR, background_rect, border_radius=8
        )

        # Selected terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 128, constants.PANEL_WIDTH - 40, 128
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Title
        self.draw_text(
            message="Deploy Troops",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player Name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops available text
        self.draw_text(
            message="Troops Available",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 90,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Actual Troops available
        self.draw_text(
            message=f"{player.reinforcements}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 110,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Selected territory and number of troops on that territory
        self.draw_text(
            message="Selected Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 160,
            font_size=24,
            font_color=constants.TEXT_COLOR
        )
        # Show the territory info if one has been selected, otherwise show none
        if selected_territory:
            self.draw_text(
                message=f"{selected_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 190,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )

            self.draw_text(
                message=f"Current Troops: {selected_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 220,
                font_size=24,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="No territory selected.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 190,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
        # Troops to deploy text
        self.draw_text(
            message="Troops to Deploy",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 280,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops to deploy counter
        self.draw_text(
            message=f"{self.deploy_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 320,
            font_size=24,
            font_color=constants.TEXT_COLOR_LIGHT
        )


    def draw_attack(self, player, attacking_territory=None, defending_territory=None):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.ATTACK_COLOR, background_rect, border_radius=8
        )
        # Attacking From rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 80, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Defending terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 185, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Title
        self.draw_text(
            message="Attack",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # "Attacking from" text
        self.draw_text(
            message="Attacking From:",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 100,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Attacking Territory info if selected
        if attacking_territory:
            self.draw_text(
                message=f"{attacking_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Attacking from territory troop count
            self.draw_text(
                message=f"Current Troops: {attacking_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 165,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Defending Territory" Text
        self.draw_text(
            message="Defending Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 200,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Defending territory info if selected
        if defending_territory:
            self.draw_text(
                message=f"{defending_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Defending territory troop count
            self.draw_text(
                message=f"Current Troops: {defending_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 265,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Attacking troops" text
        self.draw_text(
            message="Attacking Troops",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 310,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Attacking troops counter
        self.draw_text(
            message=f"{self.attack_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 345,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )

    def draw_fortify(self, player, moving_from_territory, moving_to_territory):
        # Background Rectangle
        background_rect = pygame.Rect(
            constants.PANEL_X_LEFT, constants.PANEL_Y_TOP, constants.PANEL_WIDTH, constants.PANEL_HEIGHT
        )
        pygame.draw.rect(
            self.surface, constants.FORTIFY_COLOR, background_rect, border_radius=8
        )
        # Attacking From rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 80, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Defending terr. rectangle
        selected_terr_rect = pygame.Rect(
            constants.PANEL_X_LEFT + 20, constants.PANEL_Y_TOP + 185, constants.PANEL_WIDTH - 40, 100
        )
        pygame.draw.rect(
            self.surface, constants.WHITE, selected_terr_rect, border_radius=8
        )
        # Title
        self.draw_text(
            message="Fortify",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 30,
            font_size=30,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Player name
        self.draw_text(
            message=f"{player.name}'s turn.",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 60,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # "Moving from" text
        self.draw_text(
            message="Moving From:",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 100,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Moving from Territory info if selected
        if moving_from_territory:
            self.draw_text(
                message=f"{moving_from_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Moving from territory troop count
            self.draw_text(
                message=f"Current Troops: {moving_from_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 165,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 135,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Moving to Territory" Text
        self.draw_text(
            message="Moving to Territory",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 200,
            font_size=20,
            font_color=constants.TEXT_COLOR
        )
        # Moving to territory info if selected
        if moving_to_territory:
            self.draw_text(
                message=f"{moving_to_territory.name}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=30,
                font_color=constants.TEXT_COLOR
            )
            # Moving to territory troop count
            self.draw_text(
                message=f"Current Troops: {moving_to_territory.troops}",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 265,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        else:
            self.draw_text(
                message="Please select a territory.",
                x=constants.PANEL_X_CENTER,
                y=constants.PANEL_Y_TOP + 235,
                font_size=20,
                font_color=constants.TEXT_COLOR
            )
        # "Troops to Move" text
        self.draw_text(
            message="Troops to Move",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 310,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )
        # Troops to move counter
        self.draw_text(
            message=f"{self.attack_troop_counter}",
            x=constants.PANEL_X_CENTER,
            y=constants.PANEL_Y_TOP + 345,
            font_size=20,
            font_color=constants.TEXT_COLOR_LIGHT
        )

    def on_enter(self):
        for widget in self.widgets:
            widget.show()

    def end_phase(self):
        if self.on_end_phase is not None:
            self.on_end_phase()

    def show_help(self):
        if self.on_help is not None:
            self.on_help()