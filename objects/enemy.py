import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from objects.knight import Knight

from objects.object import Object
from generation.map import Map

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim
SLIME_ATTACKSPEED = 700 ## Wait time in ms 
PROJECTILE_WARN_TIME = 400
FLASH_FREQUENCY = 1

SLIME_AGGRESSION_RADIUS = 200
SLIME_PEACE_RADIUS = 250
SLIME_ATTACK_RADIUS = 60

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
        self.spriteChangeWaitTimer = ANIMSPEED
        self.attackWaitTimer = SLIME_ATTACKSPEED
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
        pygame.draw.rect(display, (255, 0, 0), self.hitbox)
        display.blit(self.sprite, self.pos)
        for projectile in self.projectiles:
            projectile.draw(display)

SLIME_FIRST_FRAME_DOWN = 0
SLIME_IDLE_FRAME_LEFT = 4
SLIME_IDLE_FRAME_RIGHT = 8
SLIME_FIRST_FRAME_UP = 12
SLIMEIDLEFRAMES = 4
SLIME_SPEED = 0.14
SLIME_HEALTH = 3
SLIME_RECOIL_AMOUNT = 0.35

XSPRITES = 4
YSPRITES = 8

class Slime(Enemy):
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None] = None) -> None:
        super().__init__(pos, knight)
        self.spriteSize = (16, 16)
        self.size = (32, 32)
        self.hitboxSize = (30, 30)
        self.hitbox = pygame.Rect(1, 1, self.hitboxSize[0], self.hitboxSize[1])
        self.move_to_force(pos.x, pos.y)
        self.initialiseSprites("Assets\\Slimesheet.png", XSPRITES, YSPRITES, self.spriteSize)
        self.health = SLIME_HEALTH
        self.recoilAmount = SLIME_RECOIL_AMOUNT

    def initialiseSprites(self, spritesheetPath: str, xSprites: int, ySprites: int, spriteSize: tuple[int, int]) -> None:
        super().initialiseSprites(spritesheetPath, xSprites, ySprites, spriteSize)
    
    def setSprite(self, delta: int) -> None:
        self.spriteChangeWaitTimer -= delta
        if self.directionFacing == DirectionEnum.DOWN:
            self.setSpriteGivenDirection(SLIME_FIRST_FRAME_DOWN, SLIMEIDLEFRAMES)
        elif self.directionFacing == DirectionEnum.UP:
            self.setSpriteGivenDirection(SLIME_FIRST_FRAME_UP, SLIMEIDLEFRAMES)
        elif self.directionFacing == DirectionEnum.LEFT:
            self.setSpriteGivenDirection(SLIME_IDLE_FRAME_LEFT, SLIMEIDLEFRAMES)
        elif self.directionFacing == DirectionEnum.RIGHT:
            self.setSpriteGivenDirection(SLIME_IDLE_FRAME_RIGHT, SLIMEIDLEFRAMES)
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
        self.move_by(directionToPlayer.x * SLIME_SPEED * delta , directionToPlayer.y * SLIME_SPEED * delta, map)
        self.directionFacing = self.getFacingDirection(directionToPlayer)
    
    def actUponStateAttack(self, delta: int) -> None:
        self.attackWaitTimer -= delta
        if self.attackWaitTimer <= 0:
            self.attackWaitTimer = SLIME_ATTACKSPEED
            attackProjectile = SlimeAttackSlash(self.targetCoord)
            attackProjectile.passPlayerReference(self.player)
            self.projectiles.append(attackProjectile)
            self.commitedToAttack = False
            distanceToPlayer = (self.getCenter() - self.player.getCenter()).length()
            if distanceToPlayer <= SLIME_ATTACK_RADIUS:
                self.lockTarget()
    
    def lockTarget(self) -> None:
        self.targetCoord = self.player.getCenter()
        warnProjectile = SlimeAttackWarn(self.targetCoord)
        self.projectiles.append(warnProjectile)
        self.commitedToAttack = True
    
    def onHit(self, damage: int, attack_id: int) -> None:
        super().onHit(damage, attack_id)

    def changeState(self) -> None:
        distanceToPlayer = (self.getCenter() - self.player.getCenter()).length()
        if self.state == EnemyStateEnum.IDLE:
            if distanceToPlayer <= SLIME_AGGRESSION_RADIUS:
                self.state = EnemyStateEnum.PURSUIT
        elif self.state == EnemyStateEnum.PURSUIT:
            if distanceToPlayer >= SLIME_PEACE_RADIUS:
                self.state = EnemyStateEnum.IDLE
            elif distanceToPlayer <= SLIME_ATTACK_RADIUS:
                self.state = EnemyStateEnum.ATTACK
                self.attackWaitTimer = SLIME_ATTACKSPEED
                self.lockTarget()
        elif self.state == EnemyStateEnum.ATTACK and not self.commitedToAttack:
            if distanceToPlayer > SLIME_ATTACK_RADIUS:
                self.state = EnemyStateEnum.PURSUIT

DEFAULT_PROJECTILE_LIFESPAN = 200

class Projectile(Object):
    def __init__(self) -> None:
        self.lifetime = DEFAULT_PROJECTILE_LIFESPAN
        super().__init__()

    def shouldBeDestroyed(self) -> bool:
        return self.lifetime <= 0

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
        pygame.draw.rect(display, (0, 255, 255), self.hitbox)
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
