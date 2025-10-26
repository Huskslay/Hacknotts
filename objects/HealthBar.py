import pygame

SCALE = 4

class HealthBar():
    def __init__(self, display) -> None:
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

    def passPlayerReference(self, player) -> None:
        self.player = player