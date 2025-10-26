import pygame, random
from objects.object import Object

COINSPEED = 0.01

class Coin(Object):
    def __init__(self, pos: pygame.Vector2):
        self.hitbox_offset = (0, 0)
        super().__init__()
        self.spritesheet = pygame.image.load("Assets\\CoinAnim.png").convert_alpha()
        self.spritesheet = pygame.transform.scale(self.spritesheet, (14 * 7, 14))
        self.hitbox = pygame.Rect(pos.x, pos.y, 14, 14)
        self.velocity = pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10))
        if self.velocity == pygame.Vector2(0, 0):
            self.velocity = pygame.Vector2(1, 0)
        else:
            self.velocity = self.velocity.normalize()
        self.velocity *= random.randint(15, 35)
        self.totalTimeS = 0
        self.animTimer = random.randint(0, 1000)
        self.spinSpeed = random.randint(70, 400)
        self.alive = True
    
    def passPlayerReference(self, player):
        self.player = player
    
    def getDirToPlayer(self) -> pygame.Vector2:
        return (self.player.getCenter() - self.hitbox.center).normalize()

    def getFrame(self):
        frame = (int)(self.animTimer / self.spinSpeed) % 7
        return self.spritesheet.subsurface(pygame.Rect(14 * frame, 0, 14, 14))

    def update(self, delta, map, objects) -> None:
        if self.alive:
            self.animTimer += delta
            self.totalTimeS += delta * 0.001
            self.velocity *= 0.99
            self.velocity += self.getDirToPlayer() * self.totalTimeS * self.totalTimeS
            self.hitbox.x += (int) (self.velocity.x * delta * 0.01)
            self.hitbox.y += (int) (self.velocity.y * delta * 0.01)
            if self.hitbox.colliderect(self.player.hitbox):
                self.player.addCoins(1)
                self.alive = False

    
    def draw(self, display):
        if self.alive:
            display.blit(self.getFrame(), self.hitbox)
