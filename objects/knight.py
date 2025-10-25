import pygame
from enum import Enum
from objects.object import Object
from objects.enemy import Enemy
from generation.map import Map

## pee pee poo poo

ANIMSPEED = 120 ## Wait time in ms between sprite changes in anim
MOVEMENT_SPEED = 0.02
ATTACK_DURATION = 300 
MOVEMENT_SLOW_WHEN_ATTACKING = 0

FIRST_FRAME_DOWN_IDLE = 0
FIRST_FRAME_LEFT_IDLE = 18
FIRST_FRAME_RIGHT_IDLE = 12
FIRST_FRAME_UP_IDLE = 6
FIRST_FRAME_DOWN_WALK = 24
FIRST_FRAME_LEFT_WALK = 42
FIRST_FRAME_RIGHT_WALK = 36
FIRST_FRAME_UP_WALK = 30
FIRST_FRAME_DOWN_ATTACK = 96
FIRST_FRAME_RIGHT_ATTACK = 108
FIRST_FRAME_LEFT_ATTACK = 114
FIRST_FRAME_UP_ATTACK = 102
IDLE_FRAMES = 6
SWORD_HITBOX_SIZE_MULTIPLIER_WHEN_ABOVE_OR_BELOW = 1.5
HITBOX_DISTANCE_UP = 0.5
HITBOX_DISTANCE_DOWN = 1
HITBOX_DISTANCE_LEFT = 0.75
HITBOX_DISTANCE_RIGHT = 0.75

class AnimStateEnum(Enum):
    IDLE = 1
    WALK = 2
    ATTACK = 3

class DirectionEnum(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class Knight(Object):
    def __init__(self, display):

        self.size = (96, 96)
        self.spriteSize = (48, 48)
        self.hitboxSize = (24, 24)

        self.display = display
        self.spritesheet = pygame.image.load("Assets\\KnightSpritesheet.png").convert_alpha()
        self.hitbox = pygame.Rect(4, 4, self.hitboxSize[0], self.hitboxSize[1])
        self.pos = pygame.Vector2(0, 0)
        self.directionFacing = DirectionEnum.DOWN
        self.animState = AnimStateEnum.IDLE
        self.spriteChangeWaitTimer = ANIMSPEED
        self.currentSprite = 0
        self.maxHealth = 5
        self.currentHealth = 5
        self.damageCooldown = 0
        self.attacking = False
        self.attackTimer = 0
        self.spawnedAttackHitboxInCurrentAttack = False
        self.attackHitboxRect = None
        self.initialiseSprites()
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] + self.size[0] / 2
        yComponent = self.pos[1] + self.size[1] / 2
        return pygame.Vector2(xComponent, yComponent)

    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        keys = pygame.key.get_pressed()
        movementVector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movementVector += pygame.Vector2(0, -1)
        if keys[pygame.K_a]:
            movementVector += pygame.Vector2(-1, 0)
        if keys[pygame.K_s]:
            movementVector += pygame.Vector2(0, 1)
        if keys[pygame.K_d]:
            movementVector += pygame.Vector2(1, 0)
        if keys[pygame.K_SPACE]:
            self.startAttackSequence()
        if movementVector.length() != 0:
            movementVector = movementVector.normalize() * MOVEMENT_SPEED * delta * 10
        if self.attacking:
            movementVector = movementVector * MOVEMENT_SLOW_WHEN_ATTACKING
        self.move_by(movementVector.x, movementVector.y, map)
        self.handleAttackState(delta, objects)
        self.setFacingDirection(movementVector)
        self.setAnimState(movementVector)
        self.setSprite(delta)
        self.chests(map)

    def startAttackSequence(self):
        if not self.attacking:
            self.attackTimer = ATTACK_DURATION
            self.attacking = True
    
    def handleAttackState(self, delta, objects):
        self.attackTimer -= delta
        if self.attackTimer <= 0:
            self.attacking = False
            self.spawnedAttackHitboxInCurrentAttack = False
            self.attackHitboxRect = None
        if self.attacking and not self.spawnedAttackHitboxInCurrentAttack and self.attackTimer <= ATTACK_DURATION / 2:
            self.spawnedAttackHitboxInCurrentAttack = True
            self.setAttackHitbox()
        if self.attackHitboxRect != None:
            for object in objects:
                if isinstance(object, Enemy):
                    if self.attackHitboxRect.colliderect(object.hitbox):
                        object.onHit()

    def setAttackHitbox(self):
        playerRect = pygame.Rect(self.pos.x + 32, self.pos.y + 32, self.size[0] /3, self.size[1] /3)
        self.attackHitboxRect = playerRect.copy()
        match self.directionFacing:
            case DirectionEnum.UP:
                self.attackHitboxRect.move_ip(-(int)(self.attackHitboxRect.width * ((SWORD_HITBOX_SIZE_MULTIPLIER_WHEN_ABOVE_OR_BELOW -1)/2)), -(int)(playerRect.height * HITBOX_DISTANCE_UP))
                self.attackHitboxRect.size = ((int)(self.attackHitboxRect.width * SWORD_HITBOX_SIZE_MULTIPLIER_WHEN_ABOVE_OR_BELOW), self.attackHitboxRect.height)
            case DirectionEnum.DOWN:
                self.attackHitboxRect.move_ip(-(int)(self.attackHitboxRect.width * ((SWORD_HITBOX_SIZE_MULTIPLIER_WHEN_ABOVE_OR_BELOW -1)/2)), (int) (playerRect.height * HITBOX_DISTANCE_DOWN))
                self.attackHitboxRect.size = ((int)(self.attackHitboxRect.width * SWORD_HITBOX_SIZE_MULTIPLIER_WHEN_ABOVE_OR_BELOW), self.attackHitboxRect.height)
            case DirectionEnum.LEFT:
                self.attackHitboxRect.move_ip(-(int) (playerRect.width * HITBOX_DISTANCE_LEFT), 0)
            case DirectionEnum.RIGHT:
                self.attackHitboxRect.move_ip((int) (playerRect.width * HITBOX_DISTANCE_RIGHT), 0)
        
        
    def takeDamage(self, damageAmount: int) -> None:
        if self.damageCooldown > 0:
            return
        self.currentHealth -= damageAmount
        if self.currentHealth < 0:
            self.currentHealth = 0
    
    def setAnimState(self, movementVector):
        if self.attacking:
            self.animState = AnimStateEnum.ATTACK
            return
        if movementVector == pygame.Vector2(0, 0):
            self.animState = AnimStateEnum.IDLE
        else:
            self.animState = AnimStateEnum.WALK
    
    def setFacingDirection(self, movementVector):
        if movementVector == pygame.Vector2(0, 0):
            return
        else:
            movementVector = pygame.Vector2(movementVector.x, -movementVector.y)
            polarCoordinates = movementVector.as_polar()
            angle = polarCoordinates[1]
            if angle < 45 and angle > -45:
                self.directionFacing = DirectionEnum.RIGHT
            elif angle >= 45 and angle < 135:
                self.directionFacing = DirectionEnum.UP
            elif angle >= 135 or angle <= -135:
                self.directionFacing = DirectionEnum.LEFT
            else:
                self.directionFacing = DirectionEnum.DOWN

    def initialiseSprites(self) -> None:
        self.spritesheetSize = pygame.Vector2(6, 24)
        self.spriteList = []
        amountOfSprites = int(self.spritesheetSize.x * self.spritesheetSize.y)
        for spriteCount in range(0, amountOfSprites - 1):
            tempSprite = pygame.image.load("Assets\\KnightSpritesheet.png").convert_alpha()
            xCoords = (self.spriteSize[0] * (spriteCount % self.spritesheetSize.x))
            yCoords = int(spriteCount / self.spritesheetSize.x) * (self.spriteSize[0])
            tempSprite = self.spritesheet.subsurface(pygame.Rect(xCoords, yCoords, self.spriteSize[0], self.spriteSize[1]))
            tempSprite = pygame.transform.scale(tempSprite, self.size)
            self.spriteList.append(tempSprite)
    
    def setSprite(self, delta):
        self.spriteChangeWaitTimer -= delta
        if self.animState == AnimStateEnum.IDLE:
            if self.directionFacing == DirectionEnum.DOWN:
                self.setSpriteGivenDirection(FIRST_FRAME_DOWN_IDLE, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.UP:
                self.setSpriteGivenDirection(FIRST_FRAME_UP_IDLE, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.setSpriteGivenDirection(FIRST_FRAME_LEFT_IDLE, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.setSpriteGivenDirection(FIRST_FRAME_RIGHT_IDLE, IDLE_FRAMES)
        elif self.animState == AnimStateEnum.WALK:
            if self.directionFacing == DirectionEnum.DOWN:
                self.setSpriteGivenDirection(FIRST_FRAME_DOWN_WALK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.UP:
                self.setSpriteGivenDirection(FIRST_FRAME_UP_WALK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.setSpriteGivenDirection(FIRST_FRAME_LEFT_WALK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.setSpriteGivenDirection(FIRST_FRAME_RIGHT_WALK, IDLE_FRAMES)
        elif self.animState == AnimStateEnum.ATTACK:
            if self.directionFacing == DirectionEnum.DOWN:
                self.setAttackSprite(FIRST_FRAME_DOWN_ATTACK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.UP:
                self.setAttackSprite(FIRST_FRAME_UP_ATTACK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.setAttackSprite(FIRST_FRAME_LEFT_ATTACK, IDLE_FRAMES)
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.setAttackSprite(FIRST_FRAME_RIGHT_ATTACK, IDLE_FRAMES)
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
    
    def setAttackSprite(self, firstFrame, frames):
        self.currentSprite = firstFrame + (int) ((ATTACK_DURATION - self.attackTimer) / (ATTACK_DURATION / frames))

    def chests(self, map: Map) -> None:
        for chest in map.room.chests_layer.chests:
            if chest.opened: continue
            if self.hitbox.colliderect(chest.hitbox):
                chest.opened = True
                

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 0, 0), self.hitbox)
        self.display.blit(self.sprite, self.pos)
        if self.attackHitboxRect != None:
           pygame.draw.rect(display, (0, 255, 255), self.attackHitboxRect)
