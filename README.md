## Project Overview
Team: Will, Sean, Tre, Michael

We are seeking to develop a fleshed out version of the board game 'Risk! Global Domination'. All chosen rules will be based off of this version and we seek to implement full gameplay loop and local play. 

Current structure:
```
\root
    - contains constants, readme, and GameStateManager
\game
    - holds general game utility but never imports pygame itself
\assets
    - contains map images and risk_cards
\data
    - includes map data and formatted strings
\screens
    - includes all available screens, including a base_screen file template/parent
\ui
    - contains all ui functionality
\testing_files
    - contains unit tests or manual tests
```

### Setup and Usage
1. Requires Python 3.7+ **Verified on 3.12.6**
2. Set up venv
```
python3 -m venv venv
# mac/linux
source venv/bin/activate
# windows
venv\Scripts\activate
```
3. Install Required Packages (pygame, pygame_widgets) 
    - **this assumes using pip as your package manager**
    - dataclasses, pathlib, random, sys, typing, unittest are all in the python standard library
```
pip install pygame pygame_widgets
```

### Running
1. GameStateManager is the active main file.
2. The project should be run from the repo root.
```
python GameStateManager.py
```
### Expected Behavior:
Upon running GameStateManager.py, the user will load into a basic menu screen which allows them to start a new game,
continue an ongoing game, quit the program, or access the instructions.

When clicking the "New Game" button, the user is directed to a new menu where they are able to set up the parameters
for their game of Risk. The user can select between three and six players, one of which must be a bot. Players must
also all have names and a unique color identifier. If these requirements are not met, an error pops up explaining why
the user cannot proceed. If everything meets the requirements, a confirmation window will pop up, allowing the user
to verify all player information before proceeding. When confirmed, the user is directed into the actual playing screen.

The playing screen is shows the map, players in the game, and other game components. From here, players enter the
initial setup phase, where they select territories they want, and then reinforce them once all territories have been
claimed. After the initial setup phase, player's take turns in going through Risk's "Deploy", "Attack", and "Fortify"
phases. Instructions for each of these phases are noted in the panel on the right-hand side of the screen.

There is a "Help" button on the playing screen and the main menu. When clicked, the user can cycle through different
instructions pages. When leaving this screen using the "Exit" button, the user is moved back to either the playing
screen or the main menu, depending on where they were when entering the instructions menu.

While in the playing screen, hitting the "esc" key on the keyboard transports the user back to the main menu. From
there, they can either click "New Game" to begin a new game from scratch, or they can click "Continue" to resume their
current game.

The "Quit" button on the main menu screen safely exits the application.
### Testing
The following describes our available testing files and various acceptable terminal commands to run them.
```
# Dice
# Runs 13 tests to ensure functionality
python testing_files/test_dice.py
python -m unittest testing_files/test_dice.py
python -m testing_files.test_dice

# Card Features
# Runs 13 checks covering deck creation, set validation, trade values, trading and
# territory bonuses, reward cards, phase restrictions, card transfers, and discard recycling.
# Prints PASS for each check and stops at the first FAIL.
python testing_files/test_card_features.py
python -m testing_files.test_card_features

# Instructions
# Will open and allow interaction with help screen in a pygame window, shows all current rules and instructions.
python testing_files/test_instructions.py
python -m testing_files.test_instructions

# Interactive-Map
# Will open and allow interaction with the interactive map in a pygame window.
python testing_files/test_interactive_map.py
python -m testing_files.test_interactive_map
```

### Development TODOs:
1. Add requirements.txt to allow:
```
pip install -r requirements.txt
```