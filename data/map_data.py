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
        label_position=(42, 125),
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
        label_position=(125, 148),
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
        label_position=(112, 198),
    ),

    "Greenland": Territory(
        name="Greenland",
        continent="North America",
        neighbors=[
            "Northwest Territory",
            "Ontario",
            "Quebec",
            "Iceland"
        ],
        mask_color=(255, 255, 0),
        label_position=(262, 132)
    ),

    "Ontario": Territory(
        name="Ontario",
        continent="North America",
        neighbors=[
            "Northwest Territory",
            "Greenland",
            "Quebec",
            "Eastern United States",
            "Western United States",
            "Alberta"
        ],
        mask_color=(255, 0, 255),
        label_position=(153, 180)
    ),

    "Quebec": Territory(
        name="Quebec",
        continent="North America",
        neighbors=[
            "Greenland",
            "Ontario",
            "Eastern United States"
        ],
        mask_color=(0, 255, 255),
        label_position=(208, 209)
    ),

    "Western United States": Territory(
        name="Western United States",
        continent="North America",
        neighbors=[
            "Alberta",
            "Ontario",
            "Eastern United States",
            "Central America"
        ],
        mask_color=(255, 128, 0),
        label_position=(105, 264)
    ),

    "Eastern United States": Territory(
        name="Eastern United States",
        continent="North America",
        neighbors=[
            "Ontario",
            "Quebec",
            "Western United States",
            "Central America"
        ],
        mask_color=(128, 0, 255),
        label_position=(197, 250)
    ),

    "Central America": Territory(
        name="Central America",
        continent="North America",
        neighbors=[
            "Western United States",
            "Eastern United States",
            "Venezuela"
        ],
        mask_color=(0, 128, 255),
        label_position=(140, 322)
    ),

    "Venezuela": Territory(
        name="Venezuela",
        continent="South America",
        neighbors=[
            "Central America",
            "Peru",
            "Brazil"
        ],
        mask_color=(128, 255, 0),
        label_position=(163, 375)
    ),

    "Peru": Territory(
        name="Peru",
        continent="South America",
        neighbors=[
            "Venezuela",
            "Brazil",
            "Argentina"
        ],
        mask_color=(255, 0, 128),
        label_position=(147, 398)
    ),

    "Brazil": Territory(
        name="Brazil",
        continent="South America",
        neighbors=[
            "Venezuela",
            "Peru",
            "Argentina",
            "North Africa"
        ],
        mask_color=(0, 255, 128),
        label_position=(245, 440)
    ),

    "Argentina": Territory(
        name="Argentina",
        continent="South America",
        neighbors=[
            "Peru",
            "Brazil"
        ],
        mask_color=(128, 128, 255),
        label_position=(190, 515)
    ),

    "Iceland": Territory(
        name="Iceland",
        continent="Europe",
        neighbors=[
            "Greenland",
            "Great Britain",
            "Scandinavia"
        ],
        mask_color=(255, 128, 128),
        label_position=(328, 174)
    ),

    "Scandinavia": Territory(
        name="Scandinavia",
        continent="Europe",
        neighbors=[
            "Iceland",
            "Great Britain",
            "Northern Europe",
            "Ukraine"
        ],
        mask_color=(128, 255, 128),
        label_position=(394, 183)
    ),

    "Ukraine": Territory(
        name="Ukraine",
        continent="Europe",
        neighbors=[
            "Scandinavia",
            "Northern Europe",
            "Southern Europe",
            "Middle East",
            "Afghanistan",
            "Ural"
        ],
        mask_color=(128, 128, 0),
        label_position=(458, 229)
    ),

    "Great Britain": Territory(
        name="Great Britain",
        continent="Europe",
        neighbors=[
            "Iceland",
            "Scandinavia",
            "Northern Europe",
            "Western Europe"
        ],
        mask_color=(128, 0, 128),
        label_position=(330, 240)
    ),

    "Northern Europe": Territory(
        name="Northern Europe",
        continent="Europe",
        neighbors=[
            "Great Britain",
            "Scandinavia",
            "Ukraine",
            "Southern Europe",
            "Western Europe"
        ],
        mask_color=(0, 128, 128),
        label_position=(404, 220)
    ),

    "Western Europe": Territory(
        name="Western Europe",
        continent="Europe",
        neighbors=[
            "Great Britain",
            "Northern Europe",
            "Southern Europe",
            "North Africa"
        ],
        mask_color=(192, 64, 0),
        label_position=(345, 325)
    ),

    "Southern Europe": Territory(
        name="Southern Europe",
        continent="Europe",
        neighbors=[
            "Western Europe",
            "Northern Europe",
            "Ukraine",
            "Middle East",
            "Egypt",
            "North Africa"
        ],
        mask_color=(64, 0, 192),
        label_position=(412, 304)
    ),

    "North Africa": Territory(
        name="North Africa",
        continent="Africa",
        neighbors=[
            "Brazil",
            "Western Europe",
            "Southern Europe",
            "Egypt",
            "East Africa",
            "Congo"
        ],
        mask_color=(192, 0, 64),
        label_position=(360, 377)
    ),

    "Egypt": Territory(
        name="Egypt",
        continent="Africa",
        neighbors=[
            "North Africa",
            "Southern Europe",
            "Middle East",
            "East Africa"
        ],
        mask_color=(64, 192, 0),
        label_position=(404, 367)
    ),

    "East Africa": Territory(
        name="East Africa",
        continent="Africa",
        neighbors=[
            "Egypt",
            "North Africa",
            "Congo",
            "South Africa",
            "Madagascar",
            "Middle East"
        ],
        mask_color=(0, 64, 192),
        label_position=(450, 410)
    ),

    "Congo": Territory(
        name="Congo",
        continent="Africa",
        neighbors=[
            "North Africa",
            "East Africa",
            "South Africa"
        ],
        mask_color=(192, 192, 0),
        label_position=(423, 447)
    ),

    "South Africa": Territory(
        name="South Africa",
        continent="Africa",
        neighbors=[
            "Congo",
            "East Africa",
            "Madagascar"
        ],
        mask_color=(192, 0, 192),
        label_position=(430, 560)
    ),

    "Madagascar": Territory(
        name="Madagascar",
        continent="Africa",
        neighbors=[
            "South Africa",
            "East Africa"
        ],
        mask_color=(0, 192, 192),
        label_position=(520, 495)
    ),

    "Ural": Territory(
        name="Ural",
        continent="Asia",
        neighbors=[
            "Ukraine",
            "Siberia",
            "China",
            "Afghanistan"
        ],
        mask_color=(255, 192, 0),
        label_position=(545, 165)
    ),

    "Siberia": Territory(
        name="Siberia",
        continent="Asia",
        neighbors=[
            "Ural",
            "China",
            "Mongolia",
            "Irkutsk",
            "Yakutsk"
        ],
        mask_color=(255, 64, 64),
        label_position=(595, 165)
    ),

    "Yakutsk": Territory(
        name="Yakutsk",
        continent="Asia",
        neighbors=[
            "Siberia",
            "Irkutsk",
            "Kamchatka"
        ],
        mask_color=(64, 255, 64),
        label_position=(645, 135)
    ),

    "Kamchatka": Territory(
        name="Kamchatka",
        continent="Asia",
        neighbors=[
            "Yakutsk",
            "Irkutsk",
            "Mongolia",
            "Japan",
            "Alaska"
        ],
        mask_color=(64, 64, 255),
        label_position=(715, 135)
    ),

    "Irkutsk": Territory(
        name="Irkutsk",
        continent="Asia",
        neighbors=[
            "Siberia",
            "Yakutsk",
            "Kamchatka",
            "Mongolia"
        ],
        mask_color=(255, 64, 192),
        label_position=(630, 205)
    ),

    "Mongolia": Territory(
        name="Mongolia",
        continent="Asia",
        neighbors=[
            "Siberia",
            "Irkutsk",
            "Kamchatka",
            "Japan",
            "China"
        ],
        mask_color=(64, 255, 192),
        label_position=(650, 260)
    ),

    "Japan": Territory(
        name="Japan",
        continent="Asia",
        neighbors=[
            "Kamchatka",
            "Mongolia"
        ],
        mask_color=(192, 64, 255),
        label_position=(725, 265)
    ),

    "Afghanistan": Territory(
        name="Afghanistan",
        continent="Asia",
        neighbors=[
            "Ukraine",
            "Ural",
            "China",
            "India",
            "Middle East"
        ],
        mask_color=(192, 255, 64),
        label_position=(535, 275)
    ),

    "China": Territory(
        name="China",
        continent="Asia",
        neighbors=[
            "Ural",
            "Siberia",
            "Mongolia",
            "Siam",
            "India",
            "Afghanistan"
        ],
        mask_color=(255, 192, 192),
        label_position=(600, 280)
    ),

    "Middle East": Territory(
        name="Middle East",
        continent="Asia",
        neighbors=[
            "Ukraine",
            "Afghanistan",
            "India",
            "East Africa",
            "Egypt",
            "Southern Europe"
        ],
        mask_color=(192, 255, 192),
        label_position=(485, 350)
    ),

    "India": Territory(
        name="India",
        continent="Asia",
        neighbors=[
            "Middle East",
            "Afghanistan",
            "China",
            "Siam"
        ],
        mask_color=(192, 192, 255),
        label_position=(560, 315)
    ),

    "Siam": Territory(
        name="Siam",
        continent="Asia",
        neighbors=[
            "India",
            "China",
            "Indonesia"
        ],
        mask_color=(255, 128, 192),
        label_position=(629, 348)
    ),

    "Indonesia": Territory(
        name="Indonesia",
        continent="Australia",
        neighbors=[
            "Siam",
            "New Guinea",
            "Western Australia"
        ],
        mask_color=(128, 255, 192),
        label_position=(650, 465)
    ),

    "New Guinea": Territory(
        name="New Guinea",
        continent="Australia",
        neighbors=[
            "Indonesia",
            "Western Australia",
            "Eastern Australia"
        ],
        mask_color=(192, 128, 255),
        label_position=(705, 415)
    ),

    "Western Australia": Territory(
        name="Western Australia",
        continent="Australia",
        neighbors=[
            "Indonesia",
            "New Guinea",
            "Eastern Australia"
        ],
        mask_color=(255, 192, 128),
        label_position=(695, 510)
    ),

    "Eastern Australia": Territory(
        name="Eastern Australia",
        continent="Australia",
        neighbors=[
            "New Guinea",
            "Western Australia"
        ],
        mask_color=(128, 192, 255),
        label_position=(760, 555)
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
    ),

    "South America": Continent(
        name="South America",
        bonus=2,
        territories=[
            "Venezuela",
            "Peru",
            "Brazil",
            "Argentina"
        ]
    ),

    "Europe": Continent(
        name="Europe",
        bonus=5,
        territories=[
            "Iceland",
            "Scandinavia",
            "Ukraine",
            "Great Britain",
            "Northern Europe",
            "Western Europe",
            "Southern Europe"
        ]
    ),

    "Africa": Continent(
        name="Africa",
        bonus=3,
        territories=[
            "North Africa",
            "Egypt",
            "East Africa",
            "Congo",
            "South Africa",
            "Madagascar"
        ]
    ),

    "Asia": Continent(
        name="Asia",
        bonus=7,
        territories=[
            "Ural",
            "Siberia",
            "Yakutsk",
            "Kamchatka",
            "Irkutsk",
            "Mongolia",
            "Japan",
            "Afghanistan",
            "China",
            "Middle East",
            "India",
            "Siam"
        ]
    ),

    "Australia": Continent(
        name="Australia",
        bonus=2,
        territories=[
            "Indonesia",
            "New Guinea",
            "Western Australia",
            "Eastern Australia"
        ]
    )
}