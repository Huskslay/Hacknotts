SIZE = (1280, 768)
BG_SCALE = 2
TILE_SCALE = 32 * BG_SCALE


from enum import Enum

class TileEnum(Enum):
    FLOOR = 0,
    TL = 1,
    TR = 2,
    BL = 3,
    BR = 4,
    EMPTY = 5