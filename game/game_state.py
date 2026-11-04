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

        # Track the current stage of the game
        self.phase = "setup_claim"

        # True once the game has started
        self.game_started = False

        # ID of the winning player
        self.winner_id = None

        # Dictionary for starting army count based on player count
        self.starting_armies = {
            2: 40,
            3: 35,
            4: 30,
            5: 25,
            6: 20
        }

        # Remaining armies for each player during setup
        self.setup_armies = {}

    # property allows us to use current_player as a variable, but it will always return the player object for the current player index. This is useful for getting the current player without having to index into the players list manually.
    @property
    def current_player(self):
        # Return None if no players are present, otherwise return the player object for the current player index.
        if not self.players:
            return None

        return self.players[self.current_player_index]

    def add_player(self, name, color, is_bot=False):
        # Assign a unique player_id based on the current number of players
        player_id = len(self.players)

        # Create a new Player object with the provided name and color, and the assigned player_id
        player = Player(
            player_id=player_id,
            name=name,
            color=color,
            is_bot=is_bot
        )

        # Append the new player to the list of players in the game
        self.players.append(player)

        return player
    
    def claim_territory(self, territory_name):
        # Territory claiming is only allowed during setup
        if self.phase != "setup_claim":
            return False

        territory = self.territories.get(territory_name)

        # Make sure a territory is being hovered over and has no owner
        if territory is None or territory.owner_id is not None:
            return False

        player = self.current_player

        if player is None:
            return False

        # Give the territory to the current player with one troop
        self.assign_territory(
            territory_name,
            player.player_id,
            troops=1
        )

        # One starting army has now been used
        self.setup_armies[player.player_id] -= 1

        # Check whether every territory has been claimed
        all_claimed = all(
            territory.owner_id is not None
            for territory in self.territories.values()
        )

        if all_claimed:
            self.phase = "setup_place"
            self.current_player_index = 0
        else:
            self.next_player()

        return True
    
    # Simple method for advancing to the next player's turn
    def next_player(self):
        if not self.players:
            return

        self.current_player_index += 1

        # Update the current player reference to the new player at the current index
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0

    # Starts the game by setting the current player to the first player, marking the game as started, and setting the initial phase to "deploy".
    def start_game(self):
        # Start the first player's turn
        self.current_player_index = 0

        # Setup is complete
        self.game_started = True

        # Every normal turn begins with deployment
        self.phase = "deploy"   

    # Starts the setup phase of the game, ensuring the correct number of players and assigning starting armies.
    def start_setup(self):
        player_count = len(self.players)

        # Only allow games with 2-6 players
        if player_count < 2 or player_count > 6:
            return False

        army_count = self.starting_armies[player_count]

        self.current_player_index = 0
        self.phase = "setup_claim"
        self.game_started = False
        self.winner_id = None

        # Give each player their starting army supply
        self.setup_armies = {}

        for player in self.players:
            self.setup_armies[player.player_id] = army_count

        return True

    # Advances the game to the next phase, handling the transition between deploy, attack, and fortify phases.
    def next_phase(self):
        # Do not advance if the game has not started or has already ended
        if not self.game_started or self.phase == "game_over":
            return

        # Redeem cards → Calculate reinforcements → Place troops
        if self.phase == "deploy":
            self.phase = "attack"

        # Battle → Capture territories
        elif self.phase == "attack":
            self.phase = "fortify"

        # Move troops → End turn → Draw earned card
        elif self.phase == "fortify":
            self.end_turn()

    def end_turn(self):
        if not self.game_started or self.phase == "game_over":
            return

        if not self.players:
            return

        # Advance to the next player's turn
        self.next_player()

        # New turns begin with deployment
        self.phase = "deploy"

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