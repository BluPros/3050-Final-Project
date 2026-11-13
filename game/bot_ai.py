import random
from itertools import combinations

from game.cards import valid_set
from game.map_utils import reachable
from data.map_data import continents


class BotAI:
    """Chooses actions for bot players."""

    def __init__(self, difficulty="easy"):

        # edge case for invalid difficulty level
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty level")

        self.difficulty = difficulty
        self.mistake_chance = .25

    def use_random_choice(self):
        """Determine if the bot should use a random choice based on difficulty."""
        if self.difficulty == "easy":
            return True

        if self.difficulty == "medium":
            return random.random() < self.mistake_chance

        return False

    def get_owned_territories(self, game):
        """Get the territories owned by the current player."""
        player_id = game.current_player.player_id

        return [
            territory
            for territory in game.territories.values()
            if territory.owner_id == player_id
        ]

    def enemy_neighbors(self, game, territory):
        """Get the enemy territories that are neighbors of the given territory."""
        player_id = game.current_player.player_id

        return [
            game.territories[name]
            for name in territory.neighbors
            if game.territories[name].owner_id != player_id
        ]

    def allied_neighbors(self, game, territory):
        """Get the allied territories that are neighbors of the given territory."""
        player_id = game.current_player.player_id

        return [
            game.territories[name]
            for name in territory.neighbors
            if game.territories[name].owner_id == player_id
        ]

    def owns_continent(self, game, continent_name):
        """Check if the current player owns all territories in the given continent."""
        player_id = game.current_player.player_id
        continent = continents[continent_name]

        return all(
            game.territories[name].owner_id == player_id
            for name in continent.territories
        )

    def remaining_continent_enemy_territories(self, game, continent_name):
        """Get the enemy territories in the given continent that are not owned by the current player."""
        player_id = game.current_player.player_id
        continent = continents[continent_name]

        return [
            game.territories[name]
            for name in continent.territories
            if game.territories[name].owner_id != player_id
        ]

    def deploy_fortify_destination_score(self, game, territory, incoming_troops):
        """Calculate a score for deploying or fortifying troops at the given territory."""
        score = 0
        allies= self.allied_neighbors(game, territory)
        enemies = self.enemy_neighbors(game, territory)

        # +4 to heuristic score if incoming troops could save a threatened territory
        if enemies:
            strongest_enemy = max(enemy.troops for enemy in enemies)
            current_defense = territory.troops
            future_defense = current_defense + incoming_troops

            if current_defense <= strongest_enemy < future_defense:
                score += 4

        # -8 if this territory borders has no enemy territory neighbors
        if not enemies:
            score -= 8

        # +5 if this territory borders the last enemy in a continent
        remaining = self.remaining_continent_enemy_territories(game, territory.continent)

        if len(remaining) == 1:
            last_enemy = remaining[0]

            if last_enemy.name in territory.neighbors:
                score += 5

        # -3 if this territory is isolated from allies
        if not allies:
            score -= 3

        return score

    def fortify_source_score(self, game, territory):
        """Calculate a score for fortifying troops from the given source territory to the destination territory."""
        score = 0

        enemies = self.enemy_neighbors(game, territory)

        # +8 for removing troops from an interior territory
        if not enemies:
            score += 8

        # -8 for weakening a defended border of a held continen
        if enemies and self.owns_continent(game, territory.continent):
            score -= 8

        return score

    def count_player_territories(self, game, player_id):
        """Count the number of territories owned by a specific player."""
        count = 0
        for territory in game.territories.values():
            if territory.owner_id == player_id:
                count += 1
        return count

    def score_attack(self, game, source, target):
        """Calculate a score for attacking from the source territory to the target territory."""
        score = 0
        attacking_troops = source.troops - 1
        advantage = attacking_troops - target.troops
        enemy_territory_count = self.count_player_territories(game, target.owner_id)

        # +20 if the target player has only one territory, +8 if they have three or fewer territories
        if enemy_territory_count == 1:
            score += 20
        elif enemy_territory_count <= 3:
            score += 8

        # +5 if the attacking troops are more than double the target's troops
        if attacking_troops > target.troops * 2:
            score += 5

        # +3 for each troop of advantage up to a maximum of 15
        if advantage > 0:
            score += min(advantage, 5) * 3

        # +10 if the target territory is the last enemy in a continent
        remaining = self.remaining_continent_enemy_territories(game, target.continent)

        if len(remaining) == 1:
            last_enemy = remaining[0]

            if last_enemy.name == target.name:
                score += 10

        # +5 if the target is weakly defended
        if target.troops <= 2:
            score += 5

        # -8 if the attack would leave the source territory vulnerable
        other_enemies = [enemy for enemy in self.enemy_neighbors(game, source) if enemy.name != target.name]

        if other_enemies:
            strongest_enemy = max(enemy.troops for enemy in other_enemies)
            if strongest_enemy >= source.troops - 1:
                score -= 8

        # -6 when the attackers troop count is unfavorable
        if advantage < 0:
            score -= 6

        return score

    def choose_deployment(self, game):
        """Choose where to deploy reinforcements."""
        player = game.current_player
        owned = self.get_owned_territories(game)

        if not owned or player.reinforcements <= 0:
            return None

        if self.use_random_choice():
            selected = random.choice(owned)

        else:
            scores = [
                (self.deploy_fortify_destination_score
                 (game, territory, player.reinforcements), territory)
                   for territory in owned]

            best_score = max(score for score, _ in scores)

            best_territories = [territory for score, territory in scores if score == best_score]
            selected = random.choice(best_territories)

        return selected.name, player.reinforcements

    def choose_attack(self, game):
        """Choose a legal attack or decide to stop attacking."""
        player = game.current_player

        # Easy bots sometimes skip attacking.
        if self.difficulty == "easy" and random.random() < 0.25:
            return None

        possible_attacks = []

        for source in game.territories.values():
            if source.owner_id != player.player_id:
                continue

            if source.troops < 2:
                continue

            for neighbor_name in source.neighbors:
                target = game.territories[neighbor_name]

                # Cannot attack a friendly territory.
                if target.owner_id == player.player_id:
                    continue

                possible_attacks.append(
                    (source, target)
                )

        if not possible_attacks:
            return None

        if self.difficulty == "easy":
            source, target = random.choice(possible_attacks)
        else:
            scored_attacks = [
                (self.score_attack(game, source, target), source, target)
                for source, target in possible_attacks
            ]

            worthwhile = [
                entry
                for entry in scored_attacks
                if entry[0] > 0
            ]

            if not worthwhile:
                return None

            if self.use_random_choice():
                _, source, target = random.choice(worthwhile)
            else:
                best_score = max(entry[0] for entry in worthwhile)

                best_attacks = [
                    entry
                    for entry in worthwhile
                    if entry[0] == best_score
                ]
                _, source, target = random.choice(best_attacks)

        dice_count = min(3, source.troops - 1)

        return source.name, target.name, dice_count

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

        if self.difficulty == "easy":
            return random.randint(minimum_move, maximum_move)
        else:
            return maximum_move

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
        if not sources:
            return None

        possible_moves = []

        for source in sources:
            destinations = reachable(
                game.territories,
                source.name,
                player.player_id
            )

            for name in destinations:
                if name == source.name:
                    continue

                destination = game.territories[name]

                if destination.owner_id == player.player_id:
                    possible_moves.append((source, destination))

        if not possible_moves:
            return None

        if self.difficulty == "easy":
            if random.random() < 0.4:
                return None
            source, destination = random.choice(possible_moves)
            count = random.randint(1, source.troops - 1)
            return source.name, destination.name, count

        scored_moves = []
        for source, destination in possible_moves:
            count = source.troops - 1
            source_score = self.fortify_source_score(game, source)

            destination_score = self.deploy_fortify_destination_score(game, destination, count)
            score = source_score + destination_score

            if score > 0:
                scored_moves.append((score, source, destination, count))

        if not scored_moves:
            return None

        if self.use_random_choice():
            _, source, destination, count = random.choice(scored_moves)

        else:
            best_score = max(score for score, _, _, _ in scored_moves)

            best_moves = [entry for entry in scored_moves if entry[0] == best_score]
            _, source, destination, count = random.choice(best_moves)

        return source.name, destination.name, count

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
