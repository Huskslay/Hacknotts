
import pygame

from generation.rooms.start_room import StartRoom
from generation.tilemap import Tilemaps
from variables import TileEnum, TILE_SCALE

class Map:
    def __init__(self) -> None:
        self.tilemaps = Tilemaps()
        self.tilemaps.add_tilemap("transition", "Assets\\Environment\\Transition.png", TILE_SCALE, [[TileEnum.FLOOR]])
        self.tilemaps.add_tilemap("chests", "Assets\\Environment\\Chests.png", TILE_SCALE, [[TileEnum.FLOOR, TileEnum.FLOOR]])
        self.tilemaps.add_tilemap("grass", "Assets\\Environment\\TX Tileset Grass.png", TILE_SCALE,
        [
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR],
         [TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.FLOOR, TileEnum.TL, TileEnum.TR],
         ])
        
        self.room = StartRoom(self.tilemaps)

    def draw(self, display: pygame.Surface) -> None:
        self.room.draw(display)