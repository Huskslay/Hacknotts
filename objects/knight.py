import pygame
from enum import Enum
from objects.object import Object
from generation.map import Map

## pee pee poo poo

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim

FIRST_FRAME_DOWN_IDLE = 0
FIRST_FRAME_LEFT_IDLE = 18
FIRST_FRAME_RIGHT_IDLE = 12
FIRST_FRAME_UP_IDLE = 6
FIRST_FRAME_DOWN_WALK = 24
FIRST_FRAME_LEFT_WALK = 42
FIRST_FRAME_RIGHT_WALK = 36
FIRST_FRAME_UP_WALK = 30
IDLE_FRAMES = 6

class AnimStateEnum(Enum):
    IDLE = 1
    WALK = 2

class DirectionEnum(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class Knight(Object):
    def __init__(self, display):

        self.size = (96, 96)
        self.spriteSize = (48, 48)
        self.hitbox_size = (24, 24)

        self.display = display
        self.spritesheet = pygame.image.load("Assets\\KnightSpritesheet.png").convert_alpha()
        self.hitbox = pygame.Rect(0, 0, self.hitbox_size[0], self.hitbox_size[1])
        self.pos = pygame.Vector2(0, 0)
        self.directionFacing = DirectionEnum.DOWN
        self.animState = AnimStateEnum.IDLE
        self.spriteChangeWaitTimer = ANIMSPEED
        self.currentSprite = 0
        self.initialiseSprites()
        self.move_to(100, 100)
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] + self.size[0] / 2
        yComponent = self.pos[1] + self.size[1] / 2
        return pygame.Vector2(xComponent, yComponent)

    def update(self, delta: int, map: Map, objects: list[Object]) -> None:
        keys = pygame.key.get_pressed()
        movementVector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movementVector += pygame.Vector2(0, -10)
        if keys[pygame.K_a]:
            movementVector += pygame.Vector2(-10, 0)
        if keys[pygame.K_s]:
            movementVector += pygame.Vector2(0, 10)
        if keys[pygame.K_d]:
            movementVector += pygame.Vector2(10, 0)
        self.move_by(movementVector.x, movementVector.y)
        self.setFacingDirection(movementVector)
        self.setAnimState(movementVector)
        self.setSprite(delta)
    
    def setAnimState(self, movementVector):
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

    def move_by(self, x: float, y: float) -> None:
        self.move_to(self.pos.x + x, self.pos.y + y)

    def move_to(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(x + self.size[0] / 2 - self.hitbox_size[0] / 2)
        self.hitbox.y = (int)(y + self.size[1] / 2 - self.hitbox_size[1] / 2)

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

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 0, 0), self.hitbox)
        self.display.blit(self.sprite, self.pos)