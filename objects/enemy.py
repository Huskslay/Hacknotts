import pygame
from enum import Enum
from objects.object import Object

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim
ATTACKSPEED = 550 ## Wait time in ms 

SLIME_AGGRESSION_RADIUS = 250
SLIME_PEACE_RADIUS = 450
SLIME_ATTACK_RADIUS = 75

class EnemyStateEnum(Enum):
    IDLE = 1
    PURSUIT = 2
    ATTACK = 3

class DirectionEnum(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class Enemy:
    def __init__(self, display) -> None:
        self.display = display
        self.deltaTotal = 0
        self.projectiles: list[Object] = []
        self.state = EnemyStateEnum.IDLE
        self.directionFacing = DirectionEnum.UP
        self.currentSprite = 0
        self.spriteChangeWaitTimer = ANIMSPEED
        self.attackWaitTimer = ATTACKSPEED
        self.pos = pygame.Vector2(0, 0)
        self.move_to(100, 100)
        self.initialiseSprites()
    
    def passPlayerReference(self, player):
        self.player = player
    
    def initialiseSprites(self) -> None:
        self.spriteList = []
        amountOfSprites = int(self.spritesheetSize.x * self.spritesheetSize.y)
        for spriteCount in range(0, amountOfSprites - 1):
            tempSprite = pygame.image.load("Assets\\Slimesheet.png").convert_alpha()
            xCoords = (self.spriteSize[0] * (spriteCount % self.spritesheetSize.x))
            yCoords = int(spriteCount / self.spritesheetSize.x) * (self.spriteSize[0])
            tempSprite = self.spritesheet.subsurface(pygame.Rect(xCoords, yCoords, self.spriteSize[0], self.spriteSize[1]))
            tempSprite = pygame.transform.scale(tempSprite, self.size)
            self.spriteList.append(tempSprite)
    
    def getFacingDirection(self, movementVector) -> DirectionEnum:
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

    def update(self, delta: int) -> None:
        self.deltaTotal += delta
        self.setSprite(delta)
        self.handleStates(delta)
        for projectile in self.projectiles[:]:
            projectile.update(delta)
            if projectile.shouldBeDestroyed():
                self.projectiles.remove(projectile)


    def move_by(self, x: float, y: float) -> None:
        self.move_to(self.pos.x + x, self.pos.y + y)

    def setSprite(self, delta):
        pass

    def handleStates(self):
        pass

    def move_to(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(x + self.size[0] / 2 - self.hitbox_size[0] / 2)
        self.hitbox.y = (int)(y + self.size[1] / 2 - self.hitbox_size[1] / 2)

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 0, 0), self.hitbox)
        self.display.blit(self.sprite, self.pos)
        for projectile in self.projectiles:
            projectile.draw(display)

SLIME_FIRST_FRAME_DOWN = 0
SLIME_IDLE_FRAME_LEFT = 4
SLIME_IDLE_FRAME_RIGHT = 8
SLIME_FIRST_FRAME_UP = 12
SLIMEIDLEFRAMES = 4
SLIME_SPEED = 5

class Slime(Enemy):
    def __init__(self, display) -> None:
        self.spriteSize = (16, 16)
        self.size = (32, 32)
        self.hitbox_size = (30, 30)
        self.spritesheet = pygame.image.load("Assets\\Slimesheet.png").convert_alpha()
        self.hitbox = pygame.Rect(1, 1, self.hitbox_size[0], self.hitbox_size[1])
        super().__init__(display)
    
    def initialiseSprites(self) -> None:
        self.spritesheetSize = pygame.Vector2(4, 8)
        super().initialiseSprites()
    
    def setSprite(self, delta):
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
    
    def setSpriteGivenDirection(self, firstFrame, frames):
        isAnimWithinBounds = self.currentSprite < firstFrame + frames and self.currentSprite >= firstFrame
        if not isAnimWithinBounds:
            self.currentSprite = firstFrame
        if self.spriteChangeWaitTimer <= 0:
            self.spriteChangeWaitTimer = ANIMSPEED
            self.currentSprite += 1
            if self.currentSprite >= firstFrame + frames:
                self.currentSprite = firstFrame
    
    def handleStates(self, delta):
        self.changeState()
        self.actUponState(delta)
    
    def update(self, delta):
        super().update(delta)

    
    def actUponState(self, delta):
        if self.state == EnemyStateEnum.PURSUIT:
            self.actUponStatePursuit()
        elif self.state == EnemyStateEnum.ATTACK:
            self.actUponStateAttack(delta)
    
    def actUponStatePursuit(self):
        toPlayerVector = (self.player.getCenter() - self.getCenter())
        if toPlayerVector == pygame.Vector2(0, 0):
            directionToPlayer = pygame.Vector2(0, 0)
        else:
            directionToPlayer = toPlayerVector.normalize()
        self.move_by(directionToPlayer.x * SLIME_SPEED, directionToPlayer.y * SLIME_SPEED)
        self.directionFacing = self.getFacingDirection(directionToPlayer)
    
    def actUponStateAttack(self, delta):
        self.attackWaitTimer -= delta
        if self.attackWaitTimer <= 0:
            self.attackWaitTimer = ATTACKSPEED
            attackProjectile = SlimeAttackSlash(self.display, self.targetCoord)
            self.projectiles.append(attackProjectile)
            self.lockTarget()
    
    def lockTarget(self):
        self.targetCoord = self.player.getCenter()

    def changeState(self):
        distanceToPlayer = (self.getCenter() - self.player.getCenter()).length()
        if self.state == EnemyStateEnum.IDLE:
            if distanceToPlayer <= SLIME_AGGRESSION_RADIUS:
                self.state = EnemyStateEnum.PURSUIT
        elif self.state == EnemyStateEnum.PURSUIT:
            if distanceToPlayer >= SLIME_PEACE_RADIUS:
                self.state = EnemyStateEnum.IDLE
            elif distanceToPlayer <= SLIME_ATTACK_RADIUS:
                self.state = EnemyStateEnum.ATTACK
                self.attackWaitTimer = ATTACKSPEED
                self.lockTarget()
        elif self.state == EnemyStateEnum.ATTACK:
            if distanceToPlayer > SLIME_ATTACK_RADIUS:
                self.state = EnemyStateEnum.PURSUIT

class SlimeAttackSlash(Object):
    def __init__(self, display, playerCenter):

        self.size = (24, 32)
        self.hitbox_size = (24, 32)

        self.display = display
        self.sprite = pygame.image.load("Assets\\TempAttackAnim.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.hitbox = pygame.Rect(0, 0, self.hitbox_size[0], self.hitbox_size[1])
        self.pos = playerCenter - pygame.Vector2(self.size[0], self.size[1]) / 2
        self.lifetime = 200 #ms

        self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitbox_size[0] / 2)
        self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitbox_size[1] / 2)

    def shouldBeDestroyed(self) -> bool:
        return self.lifetime <= 0
    
    def update(self, delta):
        self.lifetime -= delta
    
    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (0, 255, 255), self.hitbox)
        self.display.blit(self.sprite, self.pos)
