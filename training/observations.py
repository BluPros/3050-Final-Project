from data.map_data import territories as map_territories


TERRITORY_NAMES = tuple(map_territories)
TERRITORY_INDEX = {
    name: index
    for index, name in enumerate(TERRITORY_NAMES)
}

FEATURES_PER_TERRITORY = 5
OBSERVATION_SIZE = len(TERRITORY_NAMES) * FEATURES_PER_TERRITORY

ACTION_SIZE = len(TERRITORY_NAMES) * 2 + 4


def encode_board(game):
    """Return a fixed-size observation of the current board."""
    player_id = game.current_player.player_id
    observation = []

    for name in TERRITORY_NAMES:
        territory = game.territories[name]

        is_owned = float(territory.owner_id == player_id)
        is_enemy = float(
            territory.owner_id is not None
            and territory.owner_id != player_id
        )

        enemy_neighbors = sum(
            game.territories[neighbor].owner_id != player_id
            for neighbor in territory.neighbors
        )

        observation.extend([
            is_owned,
            is_enemy,
            min(territory.troops, 100) / 100.0,
            enemy_neighbors / max(len(territory.neighbors), 1),
            min(len(territory.neighbors), 6) / 6.0
        ])

    return observation


def legal_attack_actions(game):
    """List legal attacks and the option to end the attack phase."""
    if game.phase != "attack" or game.pending_conquest is not None:
        return []

    player_id = game.current_player.player_id

    # None represents ending the attack phase.
    actions = [None]

    for name in TERRITORY_NAMES:
        source = game.territories[name]

        if source.owner_id != player_id or source.troops < 2:
            continue

        for neighbor_name in source.neighbors:
            target = game.territories[neighbor_name]

            if target.owner_id is None or target.owner_id == player_id:
                continue

            max_dice = min(3, source.troops - 1)

            for dice_count in range(1, max_dice + 1):
                actions.append(
                    (source.name, target.name, dice_count)
                )

    return actions


def encode_action(action):
    """Encode a candidate attack or the decision to stop."""
    values = [0.0] * ACTION_SIZE

    if action is None:
        values[-1] = 1.0
        return values

    source_name, target_name, dice_count = action

    source_index = TERRITORY_INDEX[source_name]
    target_index = TERRITORY_INDEX[target_name]

    values[source_index] = 1.0
    values[len(TERRITORY_NAMES) + target_index] = 1.0

    dice_start = len(TERRITORY_NAMES) * 2
    values[dice_start + dice_count - 1] = 1.0

    return values


def encode_state_action(game, action):
    """Combine the board and a candidate action for a model."""
    return encode_board(game) + encode_action(action)
