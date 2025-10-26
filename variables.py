SIZE = (1280, 768)
FPS = 60
BG_SCALE = 2
TILE_SCALE = 32 * BG_SCALE

MAP_SIZE = 8
CHEST_ROOMS = (7, 9)
TRY_SPAWN_CHESTS = (2, 5)
SHOPKEEPER_ROOMS = 3

INTERACTABLE_DISTANCE = 75
ANIMATION_SPEED_PROMPT = 220

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