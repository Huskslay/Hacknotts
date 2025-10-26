import pygame, math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.knight import Knight

SCALE = 4
COIN_RENDER_POS = (5, 50)

AMPLITUDE = 2
SPEED_FACTOR = 100.0 
STEP = 2

class HealthAndCoinBar():
    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.sprites = []
        self.totalTime = 0
        self.size = (35 * SCALE, 9 * SCALE)
        self.coinSprite = pygame.image.load("Assets\\Coin.png").convert_alpha()
        self.coinSprite = pygame.transform.scale(self.coinSprite, (10, 14))
        for n in range(0, 7):
            sprite = pygame.image.load(f"Assets\\HealthBar\\Health{n}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, self.size)
            self.sprites.append(sprite)
        self.position = pygame.Vector2(5, 5)
    
    def draw(self, delta) -> None:
        self.totalTime += delta
        healthSprite = self.sprites[self.player.currentHealth]
        self.display.blit(healthSprite, self.position)
        for n in range(0, self.player.coins):
            yOffset = AMPLITUDE * math.sin((self.totalTime / SPEED_FACTOR) + (n * STEP))
            self.display.blit(self.coinSprite, (COIN_RENDER_POS[0] + n * 6, COIN_RENDER_POS[1] + yOffset))

    def passPlayerReference(self, player: "Knight") -> None:
        self.player = player