import pygame

from objects.enemy import Enemy, Slime

class Combat:
    def __init__(self) -> None:
        self.enemies: list[Enemy] = []
        self.enemies.append(Slime(pygame.Vector2(400, 400)))