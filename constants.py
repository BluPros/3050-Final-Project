# GLobal Variables

# COLORS:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (221, 191, 138)
TEXT_COLOR = (40, 31, 24)

# WINDOW DIMS
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# INSTRUCTION STRING
INSTRUCTIONS = {
    "setup": """
SETUP

The goal is to conquer the world by occupying all 42 territories and eliminating every opponent.

Starting armies:
• 3 players: 35 armies each
• 4 players: 30 armies each
• 5 players: 25 armies each
• 6 players: 20 armies each

Claiming territories:
1. The player who rolls highest goes first.
2. Players take turns claiming unoccupied territories, placing one army on each until all 42 are claimed.
3. Players then take turns placing their remaining armies on territories they already control.
4. You may stack any number of armies on a territory.

The player who placed the first army takes the first turn.
""",

    "turn_order": """
TURN ORDER

Every turn has three phases, in this order:

1. DEPLOY
Receive and place new armies on territories you own. You may also trade in eligible Risk card sets.

2. ATTACK
Choose whether to attack enemy territories. You may attack multiple times or skip attacking entirely.

3. FORTIFY
Optionally move armies between eligible territories to strengthen your position.

After fortifying or choosing not to fortify, your turn ends.

Remember: You do not have to attack to fortify.
""",

    "deploy": """
DEPLOY

At the beginning of your turn, receive new armies based on:

TERRITORIES
Divide your number of territories by 3, rounding down. You always receive at least 3 armies.

CONTINENTS
Receive bonus armies for each continent you completely control at the start of your turn.

RISK CARDS
Trading in a valid set grants additional armies. A traded card showing a territory you own can grant 2 extra armies placed on that territory.

PLACING ARMIES
Place your reinforcements on territories you control. Use them to prepare attacks or defend your borders.
""",

    "attack": """
ATTACK

Choose an enemy territory adjacent to one you control. Dashed-line connections also count as adjacent. Alaska and Kamchatka are connected across 
the map.

REQUIREMENTS
• Your attacking territory must have at least 2 armies.
• You may attack as many times as you choose.
• You may switch targets between attacks.

DICE
Attacker: Choose 1, 2, or 3 dice. You need at least one more army than the number of dice you roll.
Defender: Chooses 1 or 2 dice. Two dice require at least 2 defending armies.

BATTLE RESULTS
The highest dice are compared first, followed by the next-highest pair if both sides rolled multiple dice. The lower die loses 1 army. Ties favor the defender. 
The attacker can lose no more than 2 armies per roll.

CAPTURING TERRITORIES
When the last defending army is defeated, you must occupy the territory immediately. Move in at least as many armies as the number of dice you rolled in 
your final battle. Leave at least 1 army in the territory you attacked from.

If you capture at least one territory during your turn, you earn 1 Risk card at the end of your turn.
""",

    "risk_cards": """
RISK CARDS

EARNING CARDS
Capture at least one territory during your turn to earn 1 Risk card. You can earn only 1 card per turn this way.

VALID SETS
• 3 cards with the same symbol.
• 3 cards with different symbols.
• 2 cards plus a Wild card.

TRADING SETS
Trade eligible sets at the beginning of your turn. If you have 5 or 6 cards at the beginning of your turn, you must trade in at least one set.

ARMY VALUES
1st set: 4 armies     4th set: 10 armies
2nd set: 6 armies    5th set: 12 armies
3rd set: 8 armies     6th set: 15 armies
Each additional set: 5 more armies than the previous set.

The value depends on how many sets all players have traded in, not just your own trades.

TERRITORY BONUS
If a traded set contains a card showing a territory you own, receive 2 extra armies on that territory. You can receive this bonus only once per turn.

ELIMINATING PLAYERS
If you eliminate an opponent, you take their Risk cards. Special trading rules apply if this gives you 6 or more cards. Follow the game's prompts.
""",

    "fortify": """
FORTIFY

At the end of your turn, you may move armies to improve your defenses or prepare for your next attack.

• Fortifying is optional.
• You do not need to attack to fortify.
• Choose one territory you own as the starting point.
• Move armies to one eligible adjacent territory you own.
• Leave at least 1 army behind in the starting territory.

You cannot move armies through enemy territories under the standard rules.

Once you finish fortifying, your turn is over.
""",

    "winning": """
WINNING THE GAME

Your objective is to conquer the world.

To win, you must eliminate every opponent by capturing all 42 territories on the board.

ELIMINATING AN OPPONENT
A player is eliminated when they lose their last army. If you eliminate a player, you receive all their Risk cards.

CONTINENT CONTROL
Owning every territory in a continent grants bonus armies at the beginning of your turn.

Protect your borders, reinforce vulnerable territories, and plan your attacks carefully.
"""
}