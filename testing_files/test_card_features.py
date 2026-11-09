import sys
from pathlib import Path


SYSTEM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))


import json

from game.game_state import Game
from game.cards import Card, valid_set, trade_value
from game.dice import RiskDice


# Creates a fresh game and starts the current player's card turn.
def create_game():
    game = Game()

    player = game.add_player(
        "Player 1",
        (150, 80, 190)
    )

    other_player = game.add_player(
        "Player 2",
        (0, 0, 255)
    )

    game.current_player_index = 0
    game.game_started = True
    game.phase = "deploy"

    return game, player, other_player


# Gives a player one card of each regular symbol.
def give_set(game, player):
    selected_cards = []

    for symbol in ("infantry", "cavalry", "artillery"):
        card = next(
            card
            for card in game.card_deck
            if card.symbol == symbol
        )

        selected_cards.append(card)

    for card in selected_cards:
        game.card_deck.remove(card)

    player.cards.extend(selected_cards)

    return [
        card.card_id
        for card in selected_cards
    ]


# Prints a failure message and stops the test script.
def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


# Checks whether an action rejects an invalid request.
def expect_value_error(action):
    try:
        action()
    except ValueError:
        return

    fail("Expected the action to raise ValueError.")


def main():
    # Check that the deck contains one card per territory and two wild cards.
    game, player, other_player = create_game()

    if len(game.card_deck) != len(game.territories) + 2:
        fail("The deck should contain one card per territory and two wild cards.")

    card_ids = {
        card.card_id
        for card in game.card_deck
    }

    if len(card_ids) != len(game.card_deck):
        fail("Each card should have a unique ID.")

    print("PASS: Deck creation")


    # Check valid and invalid card sets.
    matching_set = [
        Card("a", None, "infantry"),
        Card("b", None, "cavalry"),
        Card("c", None, "wild")
    ]

    invalid_set = [
        Card("a", None, "infantry"),
        Card("b", None, "infantry"),
        Card("c", None, "cavalry")
    ]

    if not valid_set(matching_set):
        fail("The valid card set was rejected.")

    if valid_set(invalid_set):
        fail("The invalid card set was accepted.")

    print("PASS: Card set validation")


    # Check the reinforcement values for the first eight trades.
    values = [
        trade_value(index)
        for index in range(8)
    ]

    if values != [4, 6, 8, 10, 12, 15, 20, 25]:
        fail(f"Incorrect trade values: {values}")

    print("PASS: Trade values")


    # Check that trading cards adds reinforcements and discards the cards.
    game, player, other_player = create_game()
    ids = give_set(game, player)

    result = game.redeem_card(ids)

    if result["reinforcements"] != 4:
        fail("The first trade should report four reinforcements.")

    if player.reinforcements != 4:
        fail("The player should receive four reinforcements.")

    if len(game.card_discard) != 3:
        fail("The three traded cards should be in the discard pile.")

    if player.cards != []:
        fail("The traded cards should be removed from the player's hand.")

    print("PASS: Card trading")


    # Check that an invalid trade leaves the game state unchanged.
    game, player, other_player = create_game()
    ids = give_set(game, player)

    before = game.state_snapshot()

    expect_value_error(
        lambda: game.redeem_card(
            [ids[0], ids[0], ids[1]]
        )
    )

    if before != game.state_snapshot():
        fail("An invalid trade changed the game state.")

    print("PASS: Invalid trade does not change state")


    # Check that the territory bonus is awarded only once per turn.
    game, player, other_player = create_game()
    ids = give_set(game, player)

    game.assign_territory(
        ids[0],
        player.player_id,
        troops=1
    )

    result = game.redeem_card(ids)

    if result["bonus_armies"] != 2:
        fail("The eligible territory should receive a two-army bonus.")

    if game.territories[ids[0]].troops != 3:
        fail("The territory should have three troops after the bonus.")

    ids = give_set(game, player)

    game.assign_territory(
        ids[0],
        player.player_id,
        troops=1
    )

    result = game.redeem_card(ids)

    if result["bonus_armies"] != 0:
        fail("The territory bonus should only be awarded once per turn.")

    print("PASS: Territory bonus")


    # Check that capturing a territory earns only one card per turn.
    game, player, other_player = create_game()

    game.phase = "attack"
    game.mark_territory_captured()
    game.phase = "fortify"

    first_card = game.draw_card()

    if first_card is None:
        fail("Capturing a territory should earn a reward card.")

    second_card = game.draw_card()

    if second_card is not None:
        fail("The player should not receive a second reward card.")

    if len(player.cards) != 1:
        fail("The player's hand should contain exactly one reward card.")

    print("PASS: One reward card per turn")


    # Check that no reward is given when no territory was captured.
    game, player, other_player = create_game()

    game.phase = "fortify"

    card = game.draw_card()

    if card is not None:
        fail("A player should not earn a card without capturing a territory.")

    print("PASS: No capture means no reward")


    # Check that drawing and trading are rejected in the wrong phase.
    game, player, other_player = create_game()

    ids = give_set(game, player)
    game.phase = "attack"

    expect_value_error(
        lambda: game.redeem_card(ids)
    )

    print("PASS: Card phase restrictions")


    # Check dice count, sorting, values, and invalid army counts.
    game, player, other_player = create_game()

    rolls = RiskDice("attacker").roll(armies=4, num_dice=3)

    if len(rolls) != 3:
        fail("The attacker should roll three dice.")

    if rolls != sorted(rolls, reverse=True):
        fail("Dice should be sorted from highest to lowest.")

    for value in rolls:
        if value < 1 or value > 6:
            fail("Each die should have a value between one and six.")

    expect_value_error(
        lambda: RiskDice("attacker").roll(armies=1)
    )

    print("PASS: Dice rolling")


    # Check that displayed cards and snapshots are independent copies.
    game, player, other_player = create_game()
    give_set(game, player)

    displayed_cards = game.show_card()
    displayed_cards[0]["symbol"] = "changed"

    if game.show_card()[0]["symbol"] == "changed":
        fail("Changing displayed card data changed the player's actual card.")

    snapshot = game.state_snapshot()

    # Check that the snapshot can be converted to JSON.
    try:
        json.dumps(snapshot)
    except (TypeError, ValueError):
        fail("The game snapshot could not be converted to JSON.")

    snapshot["players"][0]["territories"].append("fake")

    if "fake" in player.territories:
        fail("Changing the snapshot changed the player's actual territories.")

    print("PASS: Card display and state snapshots")


    # Check that an opponent with no territories can have their cards transferred.
    game, player, other_player = create_game()

    card = game.card_deck.pop()
    other_player.cards.append(card)

    transferred = game.transfer_cards(other_player.player_id)

    if transferred != 1:
        fail("Exactly one card should be transferred.")

    if card not in player.cards:
        fail("The transferred card is missing from the current player's hand.")

    if other_player.cards != []:
        fail("The opponent's hand should be empty after the transfer.")

    print("PASS: Card transfers")


    # Check that discarded cards are reused when the draw deck is empty.
    game, player, other_player = create_game()

    ids = give_set(game, player)
    game.redeem_card(ids)

    other_player.cards.extend(game.card_deck)
    game.card_deck.clear()

    game.phase = "attack"
    game.mark_territory_captured()
    game.phase = "fortify"

    card = game.draw_card()

    if card is None:
        fail("The player should draw a card from the recycled discard pile.")

    if len(game.card_deck) != 2:
        fail("Two cards should remain after recycling and drawing.")

    if game.card_discard != []:
        fail("The discard pile should be empty after recycling.")

    print("PASS: Discard recycling")

    print("\nAll 13 card feature checks passed.")


if __name__ == "__main__":
    main()