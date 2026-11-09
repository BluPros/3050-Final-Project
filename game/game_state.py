"""
Game Class build fresh territory objects, holds players, current_players, phases, etc.
can expose overall game functionality:
"""
from copy import deepcopy
import random

import constants
from data.map_data import territories as map_territories
from data.map_data import continents
from game.cards import make_deck, valid_set, trade_value
from game.player import Player
from game.dice import RiskDice, compare_rolls
from game.map_utils import connected

class Game:
    """Game class contains all required logic and plugs in most cooperating game elements"""
    def __init__(self):
        # This is a copy of all the territories in the game, with their
        # initial state. We will only modify the copy, not the original data.
        self.territories = deepcopy(map_territories)

        self.players = []
        self.current_player_index = 0

        # Track the current stage of the game
        self.phase = "setup_claim"

        # Card management
        self.card_deck = make_deck(self.territories)
        random.shuffle(self.card_deck)
        self.card_discard = []
        self.card_trades = 0

        # bool phase and card states
        self.captured_this_turn = False
        self.card_drawn_this_turn = False
        self.territory_bonus_used = False
        self.fortified_this_turn = False

        # True once the game has started
        self.game_started = False

        # ID of the winning player
        self.winner_id = None

        # territories in limbo
        self.pending_conquest = None

        # Dictionary for starting army count based on player count
        self.starting_armies = {
            3: 35,
            4: 30,
            5: 25,
            6: 20
        }

        # Remaining armies for each player during setup
        self.setup_armies = {}

    def reject(self, message):
        """Too many of the same annoying pattern, this is one line instead of 2,
        idk if this will actually save me time but I am annoyed so idc"""
        print(message)
        return False

    @property
    def current_player(self):
        """property allows us to use current_player as a variable, but it will always
        return the player object for the current player index. This is useful for
        getting the current player without having to index into the players list
        manually."""
        # Return None if no players are present, otherwise return the player
        # object for the current player index.
        if not self.players:
            return None

        return self.players[self.current_player_index]

    def add_player(self, name, color, is_bot=False):
        """Create player object"""
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
        """Change territory ownership if valid"""
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
            print("\n--- END OF CLAIMING ---")

            for player in self.players:
                print(
                    player.name,
                    "Territories:", len(player.territories),
                    "Remaining armies:", self.setup_armies[player.player_id]
                )
        else:
            self.next_player()

        return True

    def place_setup_army(self, territory_name):
        """Coordinate army distribution during setup"""
        # Only allow army placement during the setup phase
        if self.phase != "setup_place":
            return False

        player = self.current_player

        if player is None:
            return False

        territory = self.territories.get(territory_name)

        # Players can only reinforce territories they own
        if territory is None or territory.owner_id != player.player_id:
            return False

        # Make sure the player has armies left to place
        if self.setup_armies[player.player_id] <= 0:
            return False

        # Add one troop to the selected territory
        territory.troops += 1

        # Subtract one from the player's remaining armies
        self.setup_armies[player.player_id] -= 1

        # Check whether all players have finished placing armies
        all_placed = all(
            armies == 0
            for armies in self.setup_armies.values()
        )

        if all_placed:
            self.start_game()
        else:
            self.next_setup_player()

        return True

    def next_setup_player(self):
        """Transition to next setup player"""
        # Move to the next player who still has armies to place
        for _ in range(len(self.players)):
            self.next_player()

            player = self.current_player

            if self.setup_armies[player.player_id] > 0:
                return

    def next_player(self):
        """Method for advancing to the next player's turn"""
        if not self.players or self.phase == "game_over":
            return

        # Check each player until we find someone who can take a turn
        for _ in range(len(self.players)):

            self.current_player_index += 1

            if self.current_player_index >= len(self.players):
                self.current_player_index = 0

            # During setup, everyone gets a turn.
            # After setup, eliminated players are skipped.
            if not self.game_started or not self.current_player.eliminated:
                return

    def start_game(self):
        """Starts the game by setting the current player to the first player,
    #   marking the game as started, and setting the initial phase to "deploy"."""
        # Start the first player's turn
        self.current_player_index = 0

        # Setup is complete
        self.game_started = True

        # Start new turn
        self.start_turn()

    def start_setup(self):
        """Starts the setup phase of the game, ensuring the correct number of
        players and assigning starting armies."""
        player_count = len(self.players)

        # Only allow games with 3-6 players
        if not constants.MIN_PLAYERS <= player_count <= constants.MAX_PLAYERS:
            return False

        army_count = self.starting_armies[player_count]

        self.current_player_index = 0
        self.phase = "setup_claim"
        self.game_started = False
        self.winner_id = None

        # Give each player their starting army supply
        self.setup_armies = {}

        for player in self.players:
            player.eliminated = False
            self.setup_armies[player.player_id] = army_count

        player_card_x = constants.CARD_X_POSITIONS.get(len(self.players), [])
        x: int
        for player, x in zip(self.players, player_card_x):
            player.x_center = x

        return True

    def next_phase(self):
        """Advances the game to the next phase, handling the transition between
        deploy, attack, and fortify phases."""
        # Do not advance if the game has not started or has already ended
        if not self.game_started or self.phase == "game_over":
            return False

        if self.pending_conquest is not None:
            return False

        # Redeem cards → Calculate reinforcements → Place troops
        if self.phase == "deploy":
            if self.must_redeem_cards() or self.current_player.reinforcements > 0:
                return False
            self.phase = "attack"

        # Battle → Capture territories
        elif self.phase == "attack":
            self.phase = "fortify"

        # Move troops → End turn → Draw earned card
        elif self.phase == "fortify":
            self.end_turn()

        return True

    def start_turn(self):
        """Restart flags and phase on new_turn"""
        self.phase = "deploy"

        self.captured_this_turn = False
        self.card_drawn_this_turn = False
        self.territory_bonus_used = False
        self.fortified_this_turn = False

        self.pending_conquest = None

        player = self.current_player
        player.add_reinforcements(self.allocate_troops(player.player_id))

    def end_turn(self):
        """Ends the current player's turn, advancing to the next player"""
        if not self.game_started or self.phase == "game_over":
            return

        if not self.players:
            return

        # draw card for player
        self.draw_card()

        # Advance to the next player's turn
        self.next_player()

        # Start new turn
        self.start_turn()

    def get_player(self, player_id):
        """Simple getter for a player by their player_id. Returns None if no player
        with that id exists."""
        for player in self.players:
            if player.player_id == player_id:
                return player

        return None

    def assign_territory(self, territory_name, player_id, troops=1):
        """Assigns a territory to a player, updating the territory's owner_id and
        troops, and managing the ownership lists of the players involved."""

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

    def change_territory_owner(self, territory_name, new_player_id, incoming_troops):
        """Changes the owner of a territory to a new player, and updates the number
        of troops on that territory to match the incoming troops.
        This method is useful for handling territory ownership changes during gameplay,
        such as when a player conquers a territory from another player."""

        self.assign_territory(
            territory_name,
            new_player_id,
            incoming_troops # <-- This is the number of troops that the new owner is moving in with
        )

        # After changing ownership, check if any players have been eliminated
        # or if there is a winner
        self.check_eliminations_and_winner()


    def allocate_troops(self, player_id):
        """calculate num of troops for deployment based on owner territories
        and continents"""
        player = self.get_player(player_id)
        num_territories = len(player.territories)
        # how the game calculate number of troops awarded for territory num
        troops = num_territories // 3
        if troops < 3:
            troops = 3

        bonus = self.continent_bonus(player_id)
        troops += bonus

        return troops


    def continent_bonus(self, player_id):
        """Check continent ownership and award bonus if appropriate"""
        bonus = 0

        for continent in continents.values():
            owns = True
            for name in continent.territories:
                if self.territories[name].owner_id != player_id:
                    owns = False
                    break

            if owns:
                bonus += continent.bonus

        return bonus

    def deploy(self, territory_name, count):
        """Perform necessary checks, if all pass update territory
        with count troops added"""
        if self.phase != "deploy":
            return self.reject("not currently in deployment phase")

        player = self.current_player

        if not player.owns_territory(territory_name):
            return self.reject("current player does not own this territory")

        if count < 1:
            return self.reject("must deploy at least one troop")

        if not player.use_reinforcements(count):
            return self.reject("not enough reinforcements")

        self.territories[territory_name].add_troops(count)
        return True


    def fortify(self, src_territory, dest_territory, count):
        """Basically a BFS"""
        if self.phase != "fortify":
            return self.reject("not currently in fortify phase")

        if self.fortified_this_turn:
            return self.reject("cannot fortify more than once")

        if src_territory == dest_territory:
            return self.reject("must be different territories")

        player = self.current_player
        source = self.territories[src_territory]
        destination = self.territories[dest_territory]

        if not (player.owns_territory(dest_territory) and player.owns_territory(src_territory)):
            return self.reject("player does not own both territories")

        if source.troops <= count:
            return self.reject("not enough troops in the source territory to pull from")

        if not connected(self.territories, src_territory, dest_territory, player.player_id):
            return self.reject("territories not connected")

        source.remove_troops(count)
        destination.add_troops(count)
        self.fortified_this_turn = True
        return True

    def verify_attack(self, attacking_territory, defending_territory, num_attacking):
        """Check to make sure attack occurs on correct turn and with valid params"""
        # verify battle phase
        if self.phase != "attack":
            return self.reject("Not currently in battle phase")

        if self.pending_conquest is not None:
            return self.reject("must move troops into conquered territory")

        player = self.current_player
        attacker = self.territories[attacking_territory]
        defender = self.territories[defending_territory]

        # check validity of attack intentions
        if player is None or attacker is None or defender is None:
            return self.reject("Invalid player or territory")

        # check user holds attacking_territory
        if attacker.owner_id != player.player_id:
            return self.reject("Player does not own attacking territory")

        # check user does not hold defending territory
        if defender.owner_id == player.player_id:
            return self.reject("Player cannot control defending territory")

        # check territories are neighbors
        if not attacker.is_neighbor(defending_territory):
            return self.reject("Territories are not neighboring")


        # Verify troop_count also must be at most total troops -1
        if num_attacking >= attacker.troops:
            return self.reject("Must leave at least one army behind")
        if num_attacking > 3 or num_attacking < 1:
            return self.reject("Invalid number of attackers: must be between 1 and 3")

        return True


    def attack(self, attacking_territory, defending_territory, num_attacking):
        """Single call of attack, implements attack logic, returns true if territory
        is conquered"""
        if not self.verify_attack(attacking_territory, defending_territory, num_attacking):
            return None

        attacker = self.territories[attacking_territory]
        defender = self.territories[defending_territory]

        # create two dice which roll based on num troops
        attacking_dice = RiskDice("attacker")
        attack_roll = attacking_dice.roll(attacker.troops, num_attacking)
        defending_dice = RiskDice("defender")
        # defaults to max possible defenders
        defence_roll = defending_dice.roll(defender.troops)

        # update troop counts
        dead_attack, dead_defence = compare_rolls(attack_roll, defence_roll)
        attacker.remove_troops(dead_attack)
        defender.remove_troops(dead_defence)

        conquered = defender.troops == 0

        if conquered:
            self.pending_conquest = {
                "source": attacking_territory,
                "destination": defending_territory,
                "min_move": num_attacking
            }

        return conquered


    def move_in(self, count):
        """If attack leaves defending territory with 0 defenders
        allow user to choose how many troops to move_in with a set
        minimum determined from participating attacking troops"""
        if self.pending_conquest is None:
            return self.reject("no territory in limbo to move into")

        src_name = self.pending_conquest["source"]
        dst_name = self.pending_conquest["destination"]
        src = self.territories[src_name]
        dst = self.territories[dst_name]

        if count < self.pending_conquest["min_move"] or count > src.troops - 1:
            return self.reject("invalid number of troops to move in")

        player = self.current_player

        loser_id = dst.owner_id
        self.mark_territory_captured()
        src.remove_troops(count)
        self.change_territory_owner(dst_name, player.player_id, count)

        self.pending_conquest = None

        loser = self.get_player(loser_id)
        if loser is not None and loser.eliminated:
            self.transfer_cards(loser_id)

        return True

    def check_eliminations_and_winner(self):
        """Montitor eliminated state of each player, detect winning state"""

        # Make sure no one is elimiated before or after the start of the traditional game loop
        if not self.game_started or self.phase == "game_over":
            return

        # Check whether any player has lost all their territories to eliminate them from the game
        for player in self.players:

            if not player.eliminated and player.territory_count() == 0:
                player.eliminated = True
                print(f"{player.name} has been eliminated")

        # Find players who have not been eliminated
        active_players = [
            player for player in self.players
            if not player.eliminated
        ]

        # The last player must control the entire map to win
        if len(active_players) == 1 and all(
            territory.owner_id == active_players[0].player_id
            for territory in self.territories.values()
        ):

            winner = active_players[0]

            self.winner_id = winner.player_id
            self.phase = "game_over"

            print(f"{winner.name} has won the game!")

    def card_player(self, player_id=None):
        """Returns the requested player, or the current player if no ID is provided."""
        if player_id is None:
            player = self.current_player
        else:
            player = self.get_player(player_id)

        if player is None:
            raise ValueError("Unknown player or no current player.")

        return player


    def mark_territory_captured(self):
        """Records a successful capture so the current player can earn a card."""
        self.card_player()

        if self.phase != "attack":
            raise ValueError("Captures must occur in the attack phase.")

        self.captured_this_turn = True


    def draw_card(self):
        """Awards one card at the end of a turn if the player captured a territory."""
        player = self.card_player()

        # Players can earn only one reward card per turn.
        if not self.captured_this_turn or self.card_drawn_this_turn:
            return None

        # Reuse discarded cards if the draw deck is empty.
        if not self.card_deck and self.card_discard:
            self.card_deck = self.card_discard[:]
            self.card_discard.clear()

            random.shuffle(self.card_deck)

        if not self.card_deck:
            return None

        card = self.card_deck.pop()

        player.cards.append(card)
        self.card_drawn_this_turn = True

        return card


    def show_card(self, player_id=None):
        """Returns copies of a player's card information for the UI to display."""
        player = self.card_player(player_id)

        return [
            card.to_dict()
            for card in player.cards
        ]


    def must_redeem_cards(self):
        """Checks whether the current player has enough cards to require a trade."""
        player = self.card_player()

        return len(player.cards) >= 5


    def redeem_card(self, card_ids, bonus_territory=None):
        """Trades three valid cards for reinforcements and an eligible territory bonus."""
        player = self.card_player()

        if self.phase != "deploy":
            raise ValueError("Trade cards during deployment.")

        ids = list(card_ids)

        # A trade must contain exactly three different cards.
        if len(ids) != 3 or len(set(ids)) != 3:
            raise ValueError("Select three distinct card IDs.")

        hand = {
            card.card_id: card
            for card in player.cards
        }

        # Make sure all selected cards belong to the current player.
        if any(card_id not in hand for card_id in ids):
            raise ValueError("Selected card is not in your hand.")

        selected = [
            hand[card_id]
            for card_id in ids
        ]

        if not valid_set(selected):
            raise ValueError("Not a valid Risk card set.")

        # Find traded card territories that the current player owns.
        eligible_territories = [
            card.territory
            for card in selected
            if card.territory in self.territories
            and (
                self.territories[card.territory].owner_id
                == player.player_id
            )
        ]

        # A requested bonus must be available and match an eligible territory.
        if bonus_territory is not None:
            if (
                self.territory_bonus_used
                or bonus_territory not in eligible_territories
            ):
                raise ValueError(
                    "Territory bonus unavailable for that territory."
                )

        # Without a requested territory, use the first eligible territory.
        selected_bonus_territory = None

        if not self.territory_bonus_used:
            if bonus_territory is not None:
                selected_bonus_territory = bonus_territory
            elif eligible_territories:
                selected_bonus_territory = eligible_territories[0]

        armies = trade_value(self.card_trades)

        # Remove the traded cards from the player's hand.
        player.cards[:] = [
            card
            for card in player.cards
            if card.card_id not in ids
        ]

        self.card_discard.extend(selected)
        self.card_trades += 1

        player.add_reinforcements(armies)

        # Apply the territory bonus directly, at most once per turn.
        bonus_armies = 0

        if selected_bonus_territory is not None:
            self.territories[selected_bonus_territory].add_troops(2)

            self.territory_bonus_used = True
            bonus_armies = 2

        return {
            "reinforcements": armies,
            "bonus_territory": selected_bonus_territory,
            "bonus_armies": bonus_armies
        }


    def transfer_cards(self, eliminated_player_id):
        """Transfers an eliminated opponent's cards to the current player."""
        winner = self.card_player()
        loser = self.card_player(eliminated_player_id)

        # The current player cannot take their own cards.
        if winner is loser:
            raise ValueError("Player is not an eliminated opponent.")

        # An opponent must have no territories before their cards are transferred.
        has_territories = any(
            territory.owner_id == loser.player_id
            for territory in self.territories.values()
        )

        if has_territories:
            raise ValueError("Player is not an eliminated opponent.")

        card_count = len(loser.cards)

        winner.cards.extend(loser.cards)
        loser.cards.clear()

        return card_count


    def state_snapshot(self):
        """Returns a full state snapshot, including private hands and deck order.
        This exports data only; it does not save, load, or synchronize a game."""
        players = [
            {
                "player_id": player.player_id,
                "name": player.name,
                "color": list(player.color),
                "territories": list(player.territories),
                "reinforcements": player.reinforcements,
                "cards": [
                    card.to_dict()
                    for card in player.cards
                ]
            }
            for player in self.players
        ]

        territories = {
            name: {
                "owner_id": territory.owner_id,
                "troops": territory.troops
            }
            for name, territory in self.territories.items()
        }

        cards = {
            "deck": [
                card.to_dict()
                for card in self.card_deck
            ],
            "discard": [
                card.to_dict()
                for card in self.card_discard
            ],
            "trades": self.card_trades,
            "phase": self.phase,
            "captured": self.captured_this_turn,
            "drawn": self.card_drawn_this_turn,
            "territory_bonus_used": self.territory_bonus_used
        }

        return {
            "schema_version": 1,
            "current_player_index": self.current_player_index,
            "players": players,
            "territories": territories,
            "cards": cards
        }
