import pygame
from typing import Union

from generation.tilemap import Tilemaps
from generation.rooms.room import Room
from generation.rooms.start_room import StartRoom
from objects.object import Object

from variables import TileEnum, TILE_SCALE


class Generation(Object):
    def __init__(self) -> None:
        self.tilemaps = Tilemaps()
        self.tilemaps.add_tilemap("transition", "Assets\\Environment\\Transition.png", TILE_SCALE, [[TileEnum.FLOOR]])
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
        self.room: Union[Room, None] = None

    def go(self) -> None:
        self.room = StartRoom(self.tilemaps)

    def update(self, delta: int) -> None:
        pass

    def draw(self, display: pygame.Surface) -> None:
        if self.room == None: return
        self.room.draw(display)