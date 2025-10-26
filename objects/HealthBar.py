import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.knight import Knight

SCALE = 4

class HealthBar():
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.sprites = []
        self.size = (35 * SCALE, 9 * SCALE)
        for n in range(0, 7):
            sprite = pygame.image.load(f"Assets\\HealthBar\\Health{n}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, self.size)
            self.sprites.append(sprite)
        self.position = pygame.Vector2(5, 5)
    
    def draw(self) -> None:
        healthSprite = self.sprites[self.player.currentHealth]
        self.display.blit(healthSprite, self.position)

    def passPlayerReference(self, player: "Knight") -> None:
        self.player = player