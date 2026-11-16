
from game.game_state import Game
from training.observations import (
    OBSERVATION_SIZE,
    ACTION_SIZE,
    TERRITORY_NAMES,
    encode_board,
    encode_action,
    encode_state_action,
    legal_attack_actions
)


def main():
    """Check sizes and generate example attack choices."""
    game = Game()

    game.add_player("Easy", (255, 0, 0), is_bot=True)
    game.add_player("Medium", (0, 255, 0), is_bot=True)
    game.add_player("Hard", (0, 0, 255), is_bot=True)

    assert game.start_setup()

    # Initialize the test state.
    game.territories["Alaska"].owner_id = 0
    game.territories["Alaska"].troops = 5

    game.territories["Northwest Territory"].owner_id = 1
    game.territories["Northwest Territory"].troops = 2

    game.phase = "attack"
    game.current_player_index = 0

    board = encode_board(game)
    actions = legal_attack_actions(game)

    assert len(TERRITORY_NAMES) == 42
    assert len(board) == OBSERVATION_SIZE
    assert len(encode_action(None)) == ACTION_SIZE
    assert actions[0] is None
    assert (
        "Alaska", "Northwest Territory", 3
    ) in actions

    for action in actions:
        assert len(encode_state_action(game, action)) == (
            OBSERVATION_SIZE + ACTION_SIZE
        )

    print("Territories:", len(TERRITORY_NAMES))
    print("Board features:", len(board))
    print("Action features:", ACTION_SIZE)
    print("Combined features:", OBSERVATION_SIZE + ACTION_SIZE)
    print("Legal attack options:", len(actions))
    print("Observation tests passed.")


if __name__ == "__main__":
    main()
