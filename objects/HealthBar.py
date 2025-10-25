import pygame

class HealthBar():
    def __init__(self, display) -> None:
        self.display = display
        self.sprites = []
        self.size = (240, 120)
        for n in range(0, 6):
            sprite = pygame.image.load(f"Assets\\HealthBar\\Health{n}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, self.size)
            self.sprites.append(sprite)
        self.position = pygame.Vector2(-20, -40)
    
    def draw(self) -> None:
        healthSprite = self.sprites[self.player.currentHealth]
        self.display.blit(healthSprite, self.position)

    def passPlayerReference(self, player) -> None:
        self.player = player