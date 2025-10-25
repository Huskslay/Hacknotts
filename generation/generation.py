import pygame

from generation.map import Map
from objects.object import Object



class Generation(Object):
    def __init__(self) -> None:
        self.map = Map()

    def draw(self, display: pygame.Surface) -> None:
        self.map.draw(display)