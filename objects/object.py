import pygame

from generation.map import Map

class Object:
    def update(self, delta: int, map: Map) -> None:
        pass

    def draw(self, display: pygame.Surface) -> None:
        pass 