import pygame

from generation.map import Map
from objects.object import Object

class Object:
    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        pass

    def draw(self, display: pygame.Surface) -> None:
        pass 