import pygame
from typing import Union

from generation.map import Map
from objects.object import Object



class Generation(Object):
    def __init__(self) -> None:
        self.map = Map()

    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        pass

    def draw(self, display: pygame.Surface) -> None:
        self.map.draw(display)