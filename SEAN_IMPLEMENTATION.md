# Sean's magenta tasks

## Installation (run from your existing repository root)
Back up or commit your current work first. Copy the game and testing_files folders
from this archive into the matching folders in your project. Merge folders; do not
replace entire folders. Only the two files marked REPLACE below overwrite existing files.

- game/cards.py: NEW. Card model, deck, set validation, global trade values.
- game/sean_features.py: NEW. Game mixin with card/dice API and snapshot export.
- game/game_state.py: REPLACE your existing file. Original ownership API preserved;
  adds SeanFeatures inheritance, import, and initialization.
- game/player.py: REPLACE your existing file. Adds an independent cards list per player.
- testing_files/test_sean_features.py: NEW. Fourteen automated tests.

Leave game/dice.py, screens/playing.py, ui/map_screen.py, constants.py, and
GameStateManager.py unchanged. If teammates have edited game_state.py or player.py
since these uploads, merge just the additions rather than overwriting their work.
The directory structure follows your existing README. No extra packages required.
Use the project's verified Python 3.12 environment (existing annotations need modern Python).

## Scope and assumptions
Implements draw_card, redeem_card, show_card, roll_dice at the backend/API level.
show_card returns dictionaries for a teammate's UI; it does not display a window.
roll_dice wraps your existing RiskDice without replacing its implementation.
No battle resolution, deploy/fortify logic, setup, turn loop, bot, or win screen.
Uses your uploaded instructions' escalating global trade values and once-per-turn
owned-territory bonus. Cards use three alternating symbols in map insertion order,
plus two wilds. This assignment is a project assumption, not verified against your
card artwork. Adjust make_deck if artwork assigns different territory symbols.

state_snapshot is only a JSON-compatible full-state export for optional future
shared-state work. It is NOT multiplayer, server synchronization, save/load, or a
validated action protocol. It contains secret hands and deck order; do not broadcast
it to clients. There is no restore method or random-generator checkpoint.

Eliminated-player card transfer is provided, but the special immediate trade rules
following elimination are NOT implemented. Coordinate those with the battle/loop owner.
The loop remains responsible for player authorization, legal turn progression, and
calling hooks exactly once. Do not call begin_card_turn repeatedly within a turn.

## Integration hooks for the game-loop owner
```python
# After setup and selecting the current_player_index:
game.begin_card_turn()             # exactly once at the start of each turn

# Deploy phase: show cards and pass three selected IDs to the trade method.
hand = game.show_card()             # list of {card_id, territory, symbol}
# result = game.redeem_card([id_a, id_b, id_c])
# Optional bonus_territory=... chooses an eligible owned territory.
# Without a choice, first eligible selected territory receives +2 directly.
# Main award goes into current_player.reinforcements for deploy code to place.

# Before leaving deploy: loop should prompt while game.must_redeem_cards().
game.set_card_phase("attack")      # rejects leaving deploy with >=5 cards

# Battle owner uses this after validating attacker/defender and adjacency:
attacker_rolls = game.roll_dice("attacker", armies=4, num_dice=3)
defender_rolls = game.roll_dice("defender", armies=2, num_dice=2)
# Battle code compares rolls and updates troops/ownership itself.
# After a successful enemy conquest:
game.mark_territory_captured()
# If that eliminated an opponent: game.transfer_cards(opponent_id)

game.set_card_phase("fortify")
# Fortification is handled by the loop/fortify owner.
game.set_card_phase("end")
reward = game.draw_card()           # one card if captured; otherwise None
# Only then advance current_player_index and call begin_card_turn again.
```
The sample sequence illustrates hooks, not a complete playable turn. The uploaded
PlayingScreen still only draws/selects the map. It will not call these APIs until
buttons and a turn controller are connected. No GUI keys/buttons are added here.
Public methods raise ValueError for invalid requests; the UI should catch and display it.

## Tests
From repository root:
```
python -m unittest testing_files.test_sean_features testing_files.test_dice
```
Verified in an isolated project layout using the uploaded map/model/dice files:
14 new tests plus 13 existing dice tests, all 27 passing. This is backend validation,
not an end-to-end pygame test. Tests cover rewards, set validation, trades, bonus,
mandatory trading, invalid operations, recycling, transfer, detached snapshots, dice.
