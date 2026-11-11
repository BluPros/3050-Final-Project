
from math import comb
import random
from itertools import combinations

from game.cards import valid_set
from game.map_utils import reachable


class BotAI:
    """Base class for all bot AI implementations."""

    def __init__(self, difficulty="normal"):
        self.difficulty = difficulty

    def choose_deployment(self, game):
        # Return a legal territory and troop count
        player = game.current_player

        Owned_territories = [
            territory.name
            for territory in game.territories.values()
            if territory.owner == player.player_id
        ]

        if not Owned_territories or player.reinforcement == 0:
            return None

        return random.choice(Owned_territories), player.reinforcement

    def choose_attack(self, game):
        # Return source, target and dice count
        player = game.current_player

        # Easy bots might not attack at all
        if random.random() < 0.25:
            return None

        possible_attacks = []

        for source in game.territories.values():
            if source.owner != player.player_id:
                continue

            if source.troops < 2:
                continue

            for neighbor_name in source.adjacent:
                destination = game.territories[neighbor_name]

                if destination.owner == player.player_id:
                    continue

                possible_attacks.append((source.name, destination.name, source.troops))

        if not possible_attacks:
            return None

        source_name, destination_name = random.choice(possible_attacks)

        source = game.territories[source_name]

        dice_count = 1

        return source_name, destination_name, dice_count

    def choose_move_in(self, game):
        # Move troops after conquering territory
        conquest = game.pending_conquest

        if not conquest:
            return None

        source = game.territories[conquest["source"]]

        minimum_move = conquest["minimum_move"]
        maximum_move = source.troops - 1

        if maximum_move < minimum_move:
            return None

        return random.randint(minimum_move, maximum_move)

    def choose_fortification(self, game):
        # Return source, destination, and troop count for fortification
        player = game.current_player

        sources = [
            territory
            for territory in game.territories.values()
            if territory.owner == player.player_id and territory.troops > 1
        ]

        # Easy bots sometimes skip fortification
        if not sources or random.random() < 0.40:
            return None

        random.shuffle(sources)

        for source in sources:
            destinations = [
                name
                for name in reachable(game.territories, source.name, player.player_id)
                if name != source.name
            ]

            if not destinations:
                continue

            destination_name = random.choice(destinations)
            troop_count = random.randint(1, source.troops - 1)

            return source.name, destination_name, troop_count

        return None

    def choose_card_trade(self, game):
        # Return the cards to trade and the player to trade with
        player = game.current_player

        for cards in combinations(player.cards, 3):
            if valid_set(cards):
                return [card.card_id for card in cards]
        return None