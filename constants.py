from pathlib import Path

# Colors, Window Dimensions, Asset Paths
# COLORS:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (221, 191, 138)
TEXT_COLOR = (40, 31, 24)

# WINDOW DIMS
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# MAP LAYERS
VISIBLE_MAP = Path(__file__).parent / "assets" / "maps" / "risk_map_original.png"
MASK_MAP = Path(__file__).parent / "assets" / "maps" / "risk_map_mask.png"
