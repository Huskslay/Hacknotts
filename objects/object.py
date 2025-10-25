import pygame

from generation.map import Map

from enum import Enum

class Object:
    def update(self, delta: int, map: Map, objects: list["Object"]) -> None:
        self.hitbox : pygame.Rect
        self.hitboxSize : tuple[int, int]
        self.pos : pygame.Vector2
        self.size : tuple[int, int]

    def move_by(self, x: float, y: float) -> None:
        self.move_to(self.pos.x + x, self.pos.y + y)

    def move_to(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(x + self.size[0] / 2 - self.hitboxSize[0] / 2)
        self.hitbox.y = (int)(y + self.size[1] / 2 - self.hitboxSize[1] / 2)

    def draw(self, display: pygame.Surface) -> None:
        pass 