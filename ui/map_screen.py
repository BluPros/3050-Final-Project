import pygame

class MapScreen:

    # Initialize the MapScreen 
    def __init__(self, map_path, mask_path, game):

        # Store the game instance for later use
        self.game = game

        # Load visible map for player to see
        self.map_image = pygame.image.load(map_path).convert()

        # Load invisible territory mask for backend use
        self.mask_image = pygame.image.load(mask_path).convert()

        # Track territory that is currently underneath mouse
        self.hovered_territory = None

        # Track territory that has been clicked on (if any)
        self.selected_territory = None

        # Create a python dictionary to assign mask colors to Territory objects for quick lookup
        self.color_lookup = {}

        # Import the territory data and populate the dictionary
        for territory in self.game.territories.values():
            self.color_lookup[territory.mask_color] = territory

        self.font = pygame.font.Font(None, 30)

        # This will be a dynamic overlay that we can use to highlight territories, show troop counts, etc. It will be drawn on top of the map image.
        self.ownership_overlay = pygame.Surface(self.map_image.get_size(), pygame.SRCALPHA)
        
        self.rebuild_ownership_overlay()

    # Get the territory at a given position on the map
    def get_territory_at(self, position):
        x, y = position

        # Ensure we are within the bounds of the map
        if x < 0 or y < 0 or x >= self.mask_image.get_width() or y >= self.mask_image.get_height():
            return None

        # Get the color from the invisible map
        color = self.mask_image.get_at((x, y))

        # Convert the color to (R, G, B)
        rgb = (color.r, color.g, color.b)

        return self.color_lookup.get(rgb)
    
    # Update the hovered territory based on mouse position
    def update(self):
        mouse_position = pygame.mouse.get_pos()

        self.hovered_territory = self.get_territory_at(
            mouse_position
            )
        
    # Handle left clicks of territories
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button click
            territory = self.get_territory_at(event.pos)
            if territory is not None:
                self.selected_territory = territory
                print(f"Selected territory: {territory.name}")

    def draw(self, screen):

        # Draw the visible Risk map
        screen.blit(self.map_image, (0, 0))

        # Draw the ownership overlay on top of the map
        screen.blit(self.ownership_overlay, (0, 0))

    # Display hovered territory
        if self.hovered_territory is not None:

            text = self.font.render(
                f"Hover: {self.hovered_territory.name}",
                True,
                "black"
            )

            screen.blit(text, (20, 20))

        # Display selected territory
        if self.selected_territory is not None:

            text = self.font.render(
                f"Selected: {self.selected_territory.name}",
                True,
                "black"
            )

            screen.blit(text, (20, 50))

    # The rebuild_ownership_overlay function is responsible for updating the ownership overlay based on the current state of the game. 
    # It checks each pixel in the territory mask and colors it according to the owner of the corresponding territory.
    def rebuild_ownership_overlay(self):
        # Clear the previous ownership colors
        self.ownership_overlay.fill((0, 0, 0, 0))

        
        width = self.mask_image.get_width()
        height = self.mask_image.get_height()

        # Match territory mask colors to the owner's player color
        owner_colors = {}

        for territory in self.game.territories.values():

            # Skip territories that do not have an owner
            if territory.owner_id is None:
                continue

            player = self.game.get_player(territory.owner_id)

            # Skip if the owner ID does not match a player
            if player is None:
                continue

            owner_colors[territory.mask_color] = player.color

        # Check every pixel in the territory mask
        for y in range(height):
            for x in range(width):

                mask_pixel = self.mask_image.get_at((x, y))

                rgb = (mask_pixel.r, mask_pixel.g, mask_pixel.b)

                player_color = owner_colors.get(rgb)

                # If this pixel belongs to an owned territory,
                # color the same pixel on the transparent overlay
                if player_color is not None:
                    self.ownership_overlay.set_at(
                        (x, y),
                        (
                            player_color[0],
                            player_color[1],
                            player_color[2],
                            90
                        )
                    )
                    
