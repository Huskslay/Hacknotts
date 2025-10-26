import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union
import random

if TYPE_CHECKING:
    from objects.knight import Knight

from objects.object import Object
from generation.map import Map
from objects.enemy.enemy import Enemy, EnemyStateEnum, DirectionEnum, Projectile
from objects.coin import Coin

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim
ATTACKSPEED = 700 ## Wait time in ms 
PROJECTILE_WARN_TIME = 400
FLASH_FREQUENCY = 1

BAT_AGGRESSION_RADIUS = 200
BAT_PEACE_RADIUS = 250
BAT_ATTACK_RADIUS = 60

BAT_FIRST_FRAME_DOWN = 6
BAT_IDLE_FRAME_LEFT = 3
BAT_IDLE_FRAME_RIGHT = 9
BAT_FIRST_FRAME_UP = 0
BATIDLEFRAMES = 3
BAT_FIRST_FRAME_DOWN_ATTACK = 16
BAT_IDLE_FRAME_LEFT_ATTACK = 14
BAT_IDLE_FRAME_RIGHT_ATTACK = 18
BAT_FIRST_FRAME_UP_ATTACK = 12
BATATTACKFRAMES = 2
BAT_SPEED = 0.30
BAT_HEALTH = 2
BAT_RECOIL_AMOUNT = 1.2

XSPRITES = 3
YSPRITES = 7

class Bat(Enemy):
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None] = None) -> None:
        self.spriteChangeWaitTimer = ANIMSPEED
        super().__init__(pos, knight)
        self.spriteSize = (16, 16)
        self.size = (32, 32)
        self.isWaitingOnCoinSpawn = False
        self.hitboxSize = (30, 30)
        self.hitbox = pygame.Rect(1, 1, self.hitboxSize[0], self.hitboxSize[1])
        self.move_to_force(pos.x, pos.y)
        self.initialiseSprites("Assets\\BatSprites.png", XSPRITES, YSPRITES, self.spriteSize)
        self.health = BAT_HEALTH
        self.recoilAmount = BAT_RECOIL_AMOUNT

    def initialiseSprites(self, spritesheetPath: str, xSprites: int, ySprites: int, spriteSize: tuple[int, int]) -> None:
        super().initialiseSprites(spritesheetPath, xSprites, ySprites, spriteSize)
    
    def setSprite(self, delta: int) -> None:
        self.spriteChangeWaitTimer -= delta
        if self.state == EnemyStateEnum.IDLE:
            if self.directionFacing == DirectionEnum.DOWN:
                self.setSpriteGivenDirection(BAT_FIRST_FRAME_DOWN, BATIDLEFRAMES)
            elif self.directionFacing == DirectionEnum.UP:
                self.setSpriteGivenDirection(BAT_FIRST_FRAME_UP, BATIDLEFRAMES)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.setSpriteGivenDirection(BAT_IDLE_FRAME_LEFT, BATIDLEFRAMES)
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.setSpriteGivenDirection(BAT_IDLE_FRAME_RIGHT, BATIDLEFRAMES)
        else:
            if self.directionFacing == DirectionEnum.DOWN:
                self.setSpriteGivenDirection(BAT_FIRST_FRAME_DOWN_ATTACK, BATATTACKFRAMES)
            elif self.directionFacing == DirectionEnum.UP:
                self.setSpriteGivenDirection(BAT_FIRST_FRAME_UP_ATTACK, BATATTACKFRAMES)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.setSpriteGivenDirection(BAT_IDLE_FRAME_LEFT_ATTACK, BATATTACKFRAMES)
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.setSpriteGivenDirection(BAT_IDLE_FRAME_RIGHT_ATTACK, BATATTACKFRAMES)
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
    
    def handleStates(self, delta: int, map: Map) -> None:
        self.changeState()
        self.actUponState(delta, map)
    
    def update(self, delta, map: Map, objects: list[Object]) -> None:
        super().update(delta, map, objects)
        if self.isWaitingOnCoinSpawn:
            self.isWaitingOnCoinSpawn = False
            for _ in range(0, random.randint(8, 15)):
                coin = Coin(self.pos)
                coin.passPlayerReference(self.player)
                objects.append(coin)

        start = self.pos.copy()
        if self.recoilVelocity.length() > 0:
            self.move_by(self.recoilVelocity.x * delta, self.recoilVelocity.y * delta, map)
            self.recoilVelocity *= 0.9
            if self.recoilVelocity.length() < 0.01:
                self.recoilVelocity = pygame.Vector2(0, 0)
    
    def actUponState(self, delta: int, map: Map) -> None:
        if self.state == EnemyStateEnum.PURSUIT:
            self.actUponStatePursuit(delta, map)
        elif self.state == EnemyStateEnum.ATTACK:
            self.actUponStateAttack(delta)
    
    def actUponStatePursuit(self, delta: int, map: Map) -> None:
        toPlayerVector = (self.player.getCenter() - self.getCenter())
        if toPlayerVector == pygame.Vector2(0, 0):
            directionToPlayer = pygame.Vector2(0, 0)
        else:
            directionToPlayer = toPlayerVector.normalize()
        self.move_by(directionToPlayer.x * BAT_SPEED * delta , directionToPlayer.y * BAT_SPEED * delta, map)
        self.directionFacing = self.getFacingDirection(directionToPlayer)
    
    def actUponStateAttack(self, delta: int) -> None:
        self.attackWaitTimer -= delta
        if self.attackWaitTimer <= 0:
            self.attackWaitTimer = ATTACKSPEED
            attackProjectile = SlimeAttackSlash(self.targetCoord)
            attackProjectile.passPlayerReference(self.player)
            self.projectiles.append(attackProjectile)
            self.commitedToAttack = False
            distanceToPlayer = (self.getCenter() - self.player.getCenter()).length()
            if distanceToPlayer <= BAT_ATTACK_RADIUS:
                self.lockTarget()
    
    def lockTarget(self) -> None:
        self.targetCoord = self.player.getCenter()
        warnProjectile = SlimeAttackWarn(self.targetCoord)
        self.projectiles.append(warnProjectile)
        self.commitedToAttack = True
    
    def onHit(self, damage: int, attack_id: int) -> None:
        super().onHit(damage, attack_id)
    
    def spawnCoins(self):
        self.isWaitingOnCoinSpawn = True

    def changeState(self) -> None:
        distanceToPlayer = (self.getCenter() - self.player.getCenter()).length()
        if self.state == EnemyStateEnum.IDLE:
            if distanceToPlayer <= BAT_AGGRESSION_RADIUS:
                self.state = EnemyStateEnum.PURSUIT
        elif self.state == EnemyStateEnum.PURSUIT:
            if distanceToPlayer >= BAT_PEACE_RADIUS:
                self.state = EnemyStateEnum.IDLE
            elif distanceToPlayer <= BAT_ATTACK_RADIUS:
                self.state = EnemyStateEnum.ATTACK
                self.attackWaitTimer = ATTACKSPEED
                self.lockTarget()
        elif self.state == EnemyStateEnum.ATTACK and not self.commitedToAttack:
            if distanceToPlayer > BAT_ATTACK_RADIUS:
                self.state = EnemyStateEnum.PURSUIT


class SlimeAttackSlash(Projectile):
    def __init__(self, playerCenter: pygame.Vector2) -> None:
        super().__init__()
        self.size = (24, 32)
        self.hitboxSize = (24, 32)
        self.canDoDamage = True

        self.sprite = pygame.image.load("Assets\\TempAttackAnim.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.hitbox = pygame.Rect(0, 0, self.hitboxSize[0], self.hitboxSize[1])
        self.pos = playerCenter - pygame.Vector2(self.size[0], self.size[1]) / 2

        self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
        self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)
    
    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        self.lifetime -= delta
        if self.hitbox.colliderect(self.player.hitbox) and self.canDoDamage:
            self.player.takeDamage(1)
            self.canDoDamage = False

    def passPlayerReference(self, player: "Knight") -> None:
        self.player = player
    
    def draw(self, display: pygame.Surface) -> None:
        if __debug__: pygame.draw.rect(display, (0, 255, 255), self.hitbox)
        display.blit(self.sprite, self.pos)

class SlimeAttackWarn(Projectile):
    def __init__(self, playerCenter: pygame.Vector2) -> None:
        super().__init__()
        self.size = (24, 32)
        self.hitboxSize = (24, 32)
        self.canDoDamage = True

        self.sprite = pygame.image.load("Assets\\AttackWarn.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.hitbox = pygame.Rect(0, 0, self.hitboxSize[0], self.hitboxSize[1])
        self.pos = playerCenter - pygame.Vector2(self.size[0], self.size[1]) / 2
        self.lifetime = 400
        self.visible = True

        self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
        self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)
    
    def update(self, delta, map: Map, objects: list[Object]) -> None:
        self.lifetime -= delta
        self.visible = (int)((self.lifetime * FLASH_FREQUENCY) / 100) % 2 == 0
        
    def draw(self, display: pygame.Surface) -> None:
        if not self.visible:
            return
        display.blit(self.sprite, self.pos)
