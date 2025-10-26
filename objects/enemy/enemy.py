import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union
import random

if TYPE_CHECKING:
    from objects.knight import Knight

from objects.object import Object
from generation.map import Map

class EnemyStateEnum(Enum):
    IDLE = 1
    PURSUIT = 2
    ATTACK = 3

class DirectionEnum(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class Enemy(Object):
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None] = None) -> None:
        super().__init__()
        self.deltaTotal = 0
        self.alive = True
        self.projectiles: list[Projectile] = []
        self.sprite : pygame.Surface
        self.state = EnemyStateEnum.IDLE
        self.directionFacing = DirectionEnum.UP
        self.currentSprite = 0
        self.spriteChangeWaitTimer: int
        self.attackWaitTimer: int
        self.pos = pos
        self.spritesheet = None
        self.commitedToAttack = False
        self.health: int
        self.recoilVelocity = pygame.Vector2(0, 0)
        self.recoilAmount: float
        self.attack_immunity_id = 0

        if knight is not None: self.passPlayerReference(knight)
    
    def passPlayerReference(self, player: "Knight") -> None:
        self.player = player
    
    def onHit(self, damage: int, attack_id: int) -> None:
        if attack_id == self.attack_immunity_id: return
        self.attack_immunity_id = attack_id

        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.spawnCoins()
        else:
            self.recoilVelocity = (self.getCenter() - self.player.getCenter()).normalize() * self.recoilAmount

    
    def initialiseSprites(self, spritesheetPath: str, xSprites: int, ySprites: int, spriteSize: tuple[int, int]) -> None:
        self.spriteList = []
        self.spritesheetSize = pygame.Vector2(xSprites, ySprites)
        self.spritesheet = pygame.image.load(spritesheetPath).convert_alpha()
        amountOfSprites = (int)(self.spritesheetSize.x * self.spritesheetSize.y)
        for spriteCount in range(0, amountOfSprites - 1):
            tempSprite = pygame.image.load(spritesheetPath).convert_alpha()
            xCoords = (spriteSize[0] * (spriteCount % self.spritesheetSize.x))
            yCoords = int(spriteCount / self.spritesheetSize.x) * (spriteSize[0])
            tempSprite = self.spritesheet.subsurface(pygame.Rect(xCoords, yCoords, spriteSize[0], spriteSize[1]))
            tempSprite = pygame.transform.scale(tempSprite, self.size)
            self.spriteList.append(tempSprite)
        self.setSprite(0)

    def getFacingDirection(self, movementVector: pygame.Vector2) -> DirectionEnum:
        if movementVector == pygame.Vector2(0, 0):
            return DirectionEnum.DOWN
        else:
            movementVector = pygame.Vector2(movementVector.x, -movementVector.y)
            polarCoordinates = movementVector.as_polar()
            angle = polarCoordinates[1]
            if angle < 45 and angle > -45:
                return DirectionEnum.RIGHT
            elif angle >= 45 and angle < 135:
                return DirectionEnum.UP
            elif angle >= 135 or angle <= -135:
                return DirectionEnum.LEFT
            return DirectionEnum.DOWN
    
    def spawnCoins(self):
        pass
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] + self.size[0] / 2
        yComponent = self.pos[1] + self.size[1] / 2
        return pygame.Vector2(xComponent, yComponent)

    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        self.deltaTotal += delta
        self.setSprite(delta)
        self.handleStates(delta, map)
        for projectile in self.projectiles[:]:
            projectile.update(delta, map, objects)
            if projectile.shouldBeDestroyed():
                self.projectiles.remove(projectile)

    def setSprite(self, delta: int) -> None:
        pass

    def handleStates(self, delta: int, map: Map) -> None:
        pass

    def draw(self, display: pygame.Surface) -> None:    
        if __debug__: pygame.draw.rect(display, (255, 0, 0), self.hitbox)

        display.blit(self.sprite, self.pos)
        for projectile in self.projectiles:
            projectile.draw(display)

DEFAULT_PROJECTILE_LIFESPAN = 200

class Projectile(Object):
    def __init__(self) -> None:
        self.lifetime = DEFAULT_PROJECTILE_LIFESPAN
        super().__init__()

    def shouldBeDestroyed(self) -> bool:
        return self.lifetime <= 0