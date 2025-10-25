
import pygame

from generation.rooms.start_room import StartRoom
from generation.tilemap import Tilemaps

class Map:
    def __init__(self, tilemaps: Tilemaps) -> None:        
        self.room = StartRoom(tilemaps)

    def draw(self, display: pygame.Surface) -> None:
        self.room.draw(display)