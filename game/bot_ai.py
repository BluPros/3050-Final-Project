import random
from itertools import combinations

from game.cards import valid_set
from game.map_utils import reachable


class BotAI:
    """Chooses actions for bot players."""

    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def choose_deployment(self, game):
        """Choose where to deploy reinforcements."""
        player = game.current_player

        owned_territories = [
            territory.name
            for territory in game.territories.values()
            if territory.owner_id == player.player_id
        ]

        if not owned_territories or player.reinforcements <= 0:
            return None

        territory_name = random.choice(owned_territories)

        return territory_name, player.reinforcements

    def choose_attack(self, game):
        """Choose a legal attack or decide to stop attacking."""
        player = game.current_player

        # Easy bots sometimes skip attacking.
        if random.random() < 0.25:
            return None

        possible_attacks = []

        for source in game.territories.values():
            if source.owner_id != player.player_id:
                continue

            # At least two troops are needed to attack.
            if source.troops < 2:
                continue

            for neighbor_name in source.neighbors:
                destination = game.territories[neighbor_name]

                # Cannot attack a friendly territory.
                if destination.owner_id == player.player_id:
                    continue

                possible_attacks.append(
                    (source.name, destination.name)
                )

        if not possible_attacks:
            return None

        source_name, destination_name = random.choice(
            possible_attacks
        )

        # Use one die for now to keep conquest movement simple.
        dice_count = 1

        return source_name, destination_name, dice_count

    def choose_move_in(self, game):
        """Choose how many troops to move after a conquest."""
        conquest = game.pending_conquest

        if conquest is None:
            return None

        source = game.territories[conquest["source"]]

        minimum_move = conquest["min_move"]
        maximum_move = source.troops - 1

        if maximum_move < minimum_move:
            return None

        return random.randint(minimum_move, maximum_move)

    def choose_fortification(self, game):
        """Choose a legal fortification or skip it."""
        player = game.current_player

        sources = [
            territory
            for territory in game.territories.values()
            if territory.owner_id == player.player_id
            and territory.troops > 1
        ]

        # Easy bots sometimes skip fortification.
        if not sources or random.random() < 0.40:
            return None

        random.shuffle(sources)

        for source in sources:
            destinations = [
                name
                for name in reachable(
                    game.territories,
                    source.name,
                    player.player_id
                )
                if name != source.name
            ]

            if not destinations:
                continue

            destination_name = random.choice(destinations)
            troop_count = random.randint(
                1,
                source.troops - 1
            )

            return (
                source.name,
                destination_name,
                troop_count
            )

        return None

    def choose_card_trade(self, game):
        """Find a valid three-card set for redemption."""
        player = game.current_player

        for cards in combinations(player.cards, 3):
            if valid_set(cards):
                return [
                    card.card_id
                    for card in cards
                ]

        return None
