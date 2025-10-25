import pygame
from objects.object import Object

## Cheeky push test

class Knight(Object):
    
    def __init__(self, display):

        self.size = (96, 96)
        self.hitbox_size = (24, 24)

        self.display = display
        self.spritesheet = pygame.image.load("Assets\\KnightSpritesheet.png").convert_alpha()
        self.knightSprite = self.spritesheet.subsurface(pygame.Rect(0, 0, 48, 48))
        self.knightSprite = pygame.transform.scale(self.knightSprite, self.size)
        self.hitbox = pygame.Rect(0, 0, self.hitbox_size[0], self.hitbox_size[1])
        self.pos = pygame.Vector2(0, 0)

        self.move_to(100, 100)
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] + self.size[0] / 2
        yComponent = self.pos[1] + self.size[1] / 2
        return pygame.Vector2(xComponent, yComponent)

    def update(self, delta: int) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: # Forward
        # If W is pressed
            self.move_by(0, -10)
        
        if keys[pygame.K_a]:
            # If A is pressed
            self.move_by(-10, 0)
        
        if keys[pygame.K_s]:
            self.move_by(0, 10)
        
        if keys[pygame.K_d]:
            self.move_by(10, 0)

    def move_by(self, x: float, y: float) -> None:
        self.move_to(self.pos.x + x, self.pos.y + y)
    def move_to(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(x + self.size[0] / 2 - self.hitbox_size[0] / 2)
        self.hitbox.y = (int)(y + self.size[1] / 2 - self.hitbox_size[1] / 2)

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 0, 0), self.hitbox)
        self.display.blit(self.knightSprite, self.pos)