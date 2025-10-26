import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from objects.knight import Knight
    from generation.map import Map 

from objects.object import Object

SPRITESHEET_WIDTH = 124
SPRITESHEET_HEIGHT = 70
SPRITEHITBOXOFFSET = (23/31)
SPRITE_COLUMNS = 4
SPRITE_ROWS = 2
IDLE_FRAMES = 4
ANIMATION_SPEED = 220
ANIMATION_SPEED_PROMPT = 220
INTERACTABLE_DISTANCE = 75
PROMPT_LOCATION = (50, -18)
SPEECH_SCALE_DIV = 3
SPEECH_BUBBLE_OFFSETS = [(-50, -20), (-65, -20), (-47, -20), (-30, -55)]
SPEECH_BUBBLE_PROMPT = [(200, 0), (235, 0), (195, 0), (165, -5)]


class ShopStateEnum(Enum):
    NOT_INTERACTED = 1
    SPEAKING_DIALOGUE_1 = 2
    SPEAKING_DIALOGUE_2 = 3
    SPEAKING_DIALOGUE_3 = 4
    SPEAKING_DIALOGUE_4 = 5
    PURCHASED = 6

class Shopkeeper(Object):
    
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None]) -> None:
        super().__init__()
        
        self.spritesheet = pygame.image.load("Assets\\ShopSprites\\Shopkeeper.png").convert_alpha()
        
        self.singleSpriteWidth = SPRITESHEET_WIDTH // SPRITE_COLUMNS
        self.singleSpriteHeight = SPRITESHEET_HEIGHT // SPRITE_ROWS
        self.scaledWidth = self.singleSpriteWidth * 2
        self.scaledHeight = self.singleSpriteHeight * 2
        
        self.promptSprites = self.loadPromptSprites()
        self.speechBubbles = self.loadSpeechSprites()
        self.animationListIdle, self.animationListInteract = self.loadSprites()
        self.currentFrame = 0
        self.animationTimer = 0.0
        self.promptTimer = 0.0
        self.currentPromptFrame = 0
        self.isPromptVisible = False
        self.state = ShopStateEnum.NOT_INTERACTED
        self.eLifted = True
        
        self.sprite = self.animationListIdle[self.currentFrame]
        self.rect = self.sprite.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y + self.scaledHeight / 2, self.scaledWidth * SPRITEHITBOXOFFSET, self.scaledHeight / 2)
        
        if knight is not None: self.passPlayerReference(knight)


    def passPlayerReference(self, player: "Knight") -> None:
        self.player = player

    def getCenter(self) -> pygame.Vector2:
        xComponent = self.rect[0] + self.scaledWidth / 2
        yComponent = self.rect[1] + self.scaledHeight / 2
        return pygame.Vector2(xComponent, yComponent)

    def loadPromptSprites(self) -> list[pygame.Surface]:
        sprite1 = pygame.image.load("Assets\\ShopSprites\\EkeyPrompt.png")
        sprite2 = sprite1.subsurface(pygame.Rect(11, 0, 11, 14))
        sprite1 = sprite1.subsurface(pygame.Rect(0, 0, 11, 14))
        sprite1 = pygame.transform.scale(sprite1, (22, 28))
        sprite2 = pygame.transform.scale(sprite2, (22, 28))
        return [sprite1, sprite2]

    def loadSpeechSprites(self) -> list[pygame.Surface]:
        sprite1 = pygame.image.load("Assets\\ShopSprites\\Speech1.png")
        sprite2 = pygame.image.load("Assets\\ShopSprites\\Speech2.png")
        sprite3 = pygame.image.load("Assets\\ShopSprites\\Speech3.png")
        sprite4 = pygame.image.load("Assets\\ShopSprites\\Speech4.png")
        sprite1 = pygame.transform.scale(sprite1, (801 / SPEECH_SCALE_DIV, 180 / SPEECH_SCALE_DIV))
        sprite2 = pygame.transform.scale(sprite2, (945 / SPEECH_SCALE_DIV, 180 / SPEECH_SCALE_DIV))
        sprite3 = pygame.transform.scale(sprite3, (774 / SPEECH_SCALE_DIV, 180 / SPEECH_SCALE_DIV))
        sprite4 = pygame.transform.scale(sprite4, (630 / SPEECH_SCALE_DIV, 297 / SPEECH_SCALE_DIV))
        return [sprite1, sprite2, sprite3, sprite4]


    def loadSprites(self) -> tuple[list[pygame.Surface], list[pygame.Surface]]:
        animationListIdle = []
        animationListInteract = []
        for n in range(0, SPRITE_COLUMNS * SPRITE_ROWS):
            xCoords = (n % SPRITE_COLUMNS) * self.singleSpriteWidth
            yCoords = (n // SPRITE_COLUMNS) * self.singleSpriteHeight
            sourceRect = pygame.Rect(xCoords, yCoords, self.singleSpriteWidth, self.singleSpriteHeight)
            sprite = self.spritesheet.subsurface(sourceRect)
            sprite = pygame.transform.scale(sprite, (self.scaledWidth, self.scaledHeight))
            if n < IDLE_FRAMES:
                animationListIdle.append(sprite)
            else:
                animationListInteract.append(sprite)
        return animationListIdle, animationListInteract

    def update(self, delta: int, map: "Map", objects: list[Object]):
        self.handleAnim(delta)
        self.handlePromptAnim(delta)
        self.handleInteractions(delta)
    
    def checkIfHasEnoughMoney(self) -> bool:
        return True
    
    def handleInteractions(self, delta: int) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == ShopStateEnum.NOT_INTERACTED:
            self.state = ShopStateEnum.SPEAKING_DIALOGUE_1
            self.eLifted = False
        elif keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == ShopStateEnum.SPEAKING_DIALOGUE_1:
            self.state = ShopStateEnum.SPEAKING_DIALOGUE_2
            self.eLifted = False
        elif keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == ShopStateEnum.SPEAKING_DIALOGUE_2:
            self.state = ShopStateEnum.SPEAKING_DIALOGUE_3
            self.eLifted = False
        elif keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == ShopStateEnum.SPEAKING_DIALOGUE_3:
            self.state = ShopStateEnum.SPEAKING_DIALOGUE_4
            self.eLifted = False
        elif keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == ShopStateEnum.SPEAKING_DIALOGUE_4 and self.checkIfHasEnoughMoney():
            self.state = ShopStateEnum.PURCHASED
            self.purchasePotion()
            self.eLifted = False
        if not keys[pygame.K_e]:
            self.eLifted = True
    
    def handlePromptAnim(self, delta: int) -> None:
        if self.inRangeOfPlayer() and self.state == ShopStateEnum.NOT_INTERACTED:
            self.isPromptVisible = True
            self.promptTimer -= delta
            if self.promptTimer <= 0:
                self.promptTimer = ANIMATION_SPEED_PROMPT
                if self.currentPromptFrame == 1:
                    self.currentPromptFrame = 0
                else:
                    self.currentPromptFrame = 1
        else:
            self.isPromptVisible = False

    def purchasePotion(self) -> None:
        self.player.onPotionDrink()
    
    def inRangeOfPlayer(self) -> bool:
        return (self.player.getCenter() - self.getCenter()).length() <= INTERACTABLE_DISTANCE

    def handleAnim(self, delta: int) -> None:
        self.animationTimer += delta
        if self.animationTimer >= ANIMATION_SPEED:
            self.animationTimer = 0.0 
            self.currentFrame += 1
            if self.currentFrame >= IDLE_FRAMES:
                self.currentFrame = 0
            if self.inRangeOfPlayer():
                self.sprite = self.animationListInteract[self.currentFrame]
            else:
                self.sprite = self.animationListIdle[self.currentFrame]

    def draw(self, display: pygame.Surface) -> None:
        display.blit(self.sprite, self.rect)
        if self.isPromptVisible:
            display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + PROMPT_LOCATION[0], self.rect.y + PROMPT_LOCATION[1]))
        if self.inRangeOfPlayer():
            match self.state:
                case ShopStateEnum.SPEAKING_DIALOGUE_1:
                    display.blit(self.speechBubbles[0], (self.rect.x + SPEECH_BUBBLE_OFFSETS[0][0], self.rect.y + SPEECH_BUBBLE_OFFSETS[0][1]))
                    display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + SPEECH_BUBBLE_PROMPT[0][0], self.rect.y + SPEECH_BUBBLE_PROMPT[0][1]))
                case ShopStateEnum.SPEAKING_DIALOGUE_2:
                    display.blit(self.speechBubbles[1], (self.rect.x + SPEECH_BUBBLE_OFFSETS[1][0], self.rect.y + SPEECH_BUBBLE_OFFSETS[1][1]))
                    display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + SPEECH_BUBBLE_PROMPT[1][0], self.rect.y + SPEECH_BUBBLE_PROMPT[1][1]))
                case ShopStateEnum.SPEAKING_DIALOGUE_3:
                    display.blit(self.speechBubbles[2], (self.rect.x + SPEECH_BUBBLE_OFFSETS[2][0], self.rect.y + SPEECH_BUBBLE_OFFSETS[2][1]))
                    display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + SPEECH_BUBBLE_PROMPT[2][0], self.rect.y + SPEECH_BUBBLE_PROMPT[2][1]))
                case ShopStateEnum.SPEAKING_DIALOGUE_4:
                    display.blit(self.speechBubbles[3], (self.rect.x + SPEECH_BUBBLE_OFFSETS[3][0], self.rect.y + SPEECH_BUBBLE_OFFSETS[3][1]))
                    display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + SPEECH_BUBBLE_PROMPT[3][0], self.rect.y + SPEECH_BUBBLE_PROMPT[3][1]))
        # pygame.draw.rect(display, (255, 0, 0), self.hitbox)