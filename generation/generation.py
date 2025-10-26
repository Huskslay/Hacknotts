import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.knight import Knight

from generation.map import Map
from objects.object import Object
from generation.tilemap import Tilemaps

from variables import TileEnum, TILE_SCALE

class Generation(Object):
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
        
    def create_map(self, knight: "Knight") -> None:
        self.map = Map(self.tilemaps, knight)

    def draw(self, display: pygame.Surface) -> None:
        self.map.draw(display)