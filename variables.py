SIZE = (1280, 768)
FPS = 60
BG_SCALE = 2
TILE_SCALE = 32 * BG_SCALE

ROOM_SIZE = (10, 10)
CHEST_ROOMS = 9
TRY_SPAWN_CHESTS = 3

from enum import Enum

class TileEnum(Enum):
    FLOOR = 0,
    TL = 1,
    TR = 2,
    BL = 3,
    BR = 4,
    EMPTY = 5

class TransitionDirEnum(Enum):
    LEFT = 0,
    UP = 1,
    DOWN = 2,
    RIGHT = 3