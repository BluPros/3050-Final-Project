import pygame

from data.map_data import territories, continents

class MapScreen:
  
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

    