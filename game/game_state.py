# Game Class
# Should build fresh Territory objects, hold players and curernt_player, and phase
# Can expose functionality:
# attack(src, dst, n_dice)
# fortify(...)

# Playing screen would likely own one Game

#############################################
from copy import deepcopy

from data.map_data import territories as map_territories
from game.player import Player


class Game:
    def __init__(self):
        # This is a copy of all the territories in the game, with their initial state. We will only modify the copy, not the original data.
        self.territories = deepcopy(map_territories)

        self.players = []
        self.current_player_index = 0

    # property allows us to use curren_player as a variable, but it will always return the player object for the current player index. This is useful for getting the current player without having to index into the players list manually.
    @property
    def current_player(self):
        # Return None if no players are present, otherwise return the player object for the current player index.
        if not self.players:
            return None

        return self.players[self.current_player_index]

    def add_player(self, name, color):
        # Assign a unique player_id based on the current number of players
        player_id = len(self.players)

        # Create a new Player object with the provided name and color, and the assigned player_id
        player = Player(
            player_id=player_id,
            name=name,
            color=color
        )

        # Append the new player to the list of players in the game
        self.players.append(player)

        return player

    # Simple getter for a player by their player_id. Returns None if no player with that id exists.
    def get_player(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player

        return None

    # Assigns a territory to a player, updating the territory's owner_id and troops, and managing the ownership lists of the players involved.
    def assign_territory(self, territory_name, player_id, troops=1):

        # Find the territory object by its name in the territories dictionary
        territory = self.territories[territory_name]

        # Remove territory from previous owner's list
        if territory.owner_id is not None:
            old_owner = self.get_player(territory.owner_id)

            if old_owner is not None:
                old_owner.remove_territory(territory_name)

        # Assign new owner and troops to the territory
        territory.owner_id = player_id
        territory.troops = troops

        # Add territory to new owner's list
        new_owner = self.get_player(player_id)
        if new_owner is not None:
            new_owner.add_territory(territory_name)

    # Changes the owner of a territory to a new player, and updates the number of troops on that territory to match the incoming troops. 
    # This method is useful for handling territory ownership changes during gameplay, such as when a player conquers a territory from another player.
    def change_territory_owner(self, territory_name, new_player_id, incoming_troops):

        self.assign_territory(
            territory_name,
            new_player_id,
            incoming_troops # <-- This is the number of troops that the new owner is moving in with
        )