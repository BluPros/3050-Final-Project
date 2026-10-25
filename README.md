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
Expected Behavior:
Upon running GameStateManager.py the user will load into a basic menu screen which allows navigation to our two active components; Instructions('Help'), InteractiveMap('Play'), current functionality limits menu control, i.e. we are missing a back button from the playing screen and currently the playing screen does not offer means to access the instructions, but further development will address both concerns. 

### Testing
The following describes our available testing files and various acceptable terminal commands to run them.
```
# Dice
# Runs 13 tests to ensure functionality
python testing_files/test_dice.py
python -m unittest testing_files/test_dice.py
python -m testing_files.test_dice

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