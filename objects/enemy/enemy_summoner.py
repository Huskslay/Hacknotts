import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union, Type
import random

if TYPE_CHECKING:
    from objects.knight import Knight
    from generation.rooms.room import Room

from objects.object import Object
from generation.map import Map
from objects.enemy.enemy import Enemy, EnemyStateEnum, DirectionEnum, Projectile
from objects.coin import Coin

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim
SLIME_ATTACKSPEED = 700 ## Wait time in ms 
PROJECTILE_WARN_TIME = 400
FLASH_FREQUENCY = 1

SLIME_AGGRESSION_RADIUS = 200
SLIME_PEACE_RADIUS = 250
SLIME_ATTACK_RADIUS = 60

SLIME_FIRST_FRAME_DOWN = 0
SLIME_IDLE_FRAME_LEFT = 4
SLIME_IDLE_FRAME_RIGHT = 8
SLIME_FIRST_FRAME_UP = 12
SLIMEIDLEFRAMES = 4
SLIME_SPEED = 0.14
HEALTH = 9999999
RECOIL_AMOUNT = 0

XSPRITES = 6
YSPRITES = 1

class EnemySummoner(Enemy):
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None] = None) -> None:
        self.hitbox_offset = (0, 0)
        self.spriteChangeWaitTimer = ANIMSPEED
        super().__init__(pos, knight)
        self.spriteSize = (32, 32)
        self.size = (64, 64)
        self.isWaitingOnCoinSpawn = False
        self.hitboxSize = (0, 0)
        self.hitbox = pygame.Rect(1, 1, self.hitboxSize[0], self.hitboxSize[1])
        self.move_to_force(pos.x, pos.y)
        self.initialiseSprites("Assets\\EnemySpawnerSprites.png", XSPRITES, YSPRITES, self.spriteSize)
        self.health = HEALTH
        self.recoilAmount = RECOIL_AMOUNT
        self.active = False

    def go(self, room: "Room", to_spawn: list[Type[Enemy]]) -> None:
        self.room = room
        self.active = True
        self.timer = 5000
        self.to_spawn = to_spawn

    def initialiseSprites(self, spritesheetPath: str, xSprites: int, ySprites: int, spriteSize: tuple[int, int]) -> None:
        super().initialiseSprites(spritesheetPath, xSprites, ySprites, spriteSize)
    
    def setSprite(self, delta: int) -> None:
        self.spriteChangeWaitTimer -= delta
        self.setSpriteGivenDirection(0, 5)
        self.sprite = self.spriteList[self.currentSprite]

    def setSpriteGivenDirection(self, firstFrame: int, frames: int) -> None:
        isAnimWithinBounds = self.currentSprite < firstFrame + frames and self.currentSprite >= firstFrame
        if not isAnimWithinBounds:
            self.currentSprite = firstFrame
        if self.spriteChangeWaitTimer <= 0:
            self.spriteChangeWaitTimer = ANIMSPEED
            self.currentSprite += 1
            if self.currentSprite >= firstFrame + frames:
                self.currentSprite = firstFrame
    
    def update(self, delta, map: Map, objects: list[Object]) -> None:
        if not self.active: return
        super().update(delta, map, objects)

        self.timer -= delta
        if self.timer <= 0:
            if self.to_spawn == []:
                self.alive = False
                return
            inst = self.to_spawn.pop(0)(pygame.Vector2(
                self.pos.x + random.randint(-10, 10), 
                self.pos.y + random.randint(-10, 10)), self.player
            )
            self.room.objects.append(inst)
            self.timer = 500

    def draw(self, display: pygame.Surface) -> None:
        if not self.active: return
        return super().draw(display)
    
    def onHit(self, damage: float, attack_id: int) -> None:
        return