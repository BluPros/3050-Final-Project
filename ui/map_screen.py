import pygame

from data.map_data import territories, continents

class MapScreen:

    # Initialize the MapScreen 
    def __init__(self, map_path, mask_path):

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

        # Import the territory data from map_data.py and populate the dictionary
        for territory in territories.values():
            self.color_lookup[territory.mask_color] = territory

        self.font = pygame.font.Font(None, 30)

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
            territory = self.get_territory_at(pygame.mouse.get_pos())
            if territory is not None:
                self.selected_territory = territory
                print(f"Selected territory: {territory.name}")

    def draw(self, screen):

    # Draw the visible Risk map
        screen.blit(self.map_image, (0, 0))

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