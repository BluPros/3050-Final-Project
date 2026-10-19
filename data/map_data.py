from game.territory import Territory
from game.continent import Continent

# Going to hardcode the map data as making this importable is not necessary for our scope

territories = {
    "Alaska": Territory(
        name="Alaska",
        continent="North America",
        neighbors=[
            "Northwest Territory", 
            "Alberta", 
            "Kamchatka"
            ],
        mask_color=(255, 0, 0),
        label_position=(50, 70),
    ),
    "Northwest Territory": Territory(
        name="Northwest Territory",
        continent="North America",
        neighbors=[
            "Alaska", 
            "Alberta", 
            "Ontario", 
            "Greenland"
        ],
        mask_color=(0, 255, 0),
        label_position=(125, 70),
    ),
    "Alberta": Territory(
        name="Alberta",
        continent="North America",
        neighbors=[
            "Alaska", 
            "Northwest Territory",
            "Ontario",
            "Western United States"
        ],
        mask_color=(0, 0, 255),
        label_position=(105, 105),
    ),
}

continents = {
    "North America": Continent(
        name="North America",
        bonus=5,
        territories=[
            "Alaska",
            "Northwest Territory",
            "Alberta",
            "Ontario",
            "Quebec",
            "Greenland",
            "Western United States",
            "Eastern United States",
            "Central America"
        ]
    )
}