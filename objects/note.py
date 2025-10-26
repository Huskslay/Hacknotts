import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from objects.knight import Knight
    from generation.map import Map 

from objects.object import Object
from variables import INTERACTABLE_DISTANCE, ANIMATION_SPEED_PROMPT

COINSPEED = 0.01
WIDTH = 17
HEIGHT = 7

PROMPT_LOCATION = (-20, -20)
UIPOS = (300, 40)
TEXTPOS = (420, 220)
TEXTPOS2 = (420, 280)


class NoteEnum(Enum):
    NOT_INTERACTING = 1
    INTERACTING = 2

class Note(Object):
    
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None]) -> None:
        super().__init__()
        self.spritemain = pygame.image.load("Assets\\NoteUI.png")
        self.spritemain = pygame.transform.scale(self.spritemain, (650, 650))
        self.sprite1 = pygame.image.load("Assets\\NoteFloor.png")
        self.sprite2 = self.sprite1.subsurface(pygame.Rect(17, 0, 17, 7))
        self.sprite1 = self.sprite1.subsurface(pygame.Rect(0, 0, 17, 7))
        self.sprite1 = pygame.transform.scale(self.sprite1, (34, 14))
        self.sprite2 = pygame.transform.scale(self.sprite2, (34, 14))
        self.promptSprites = self.loadPromptSprites()
        self.scaledWidth = WIDTH * 2
        self.scaledHeight = HEIGHT * 2
        self.state = NoteEnum.NOT_INTERACTING
        self.rect = self.sprite1.get_rect(topleft=pos)
        self.fontObject = pygame.font.SysFont('Arial', 60)
        self.fontObject2 = pygame.font.SysFont('Arial', 20)
        self.promptTimer = 0
        self.currentPromptFrame = 0
        self.deltaTotal = 0
        self.passPlayerReference(knight)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.scaledWidth, self.scaledHeight)
    
    def update(self, delta: int, map: "Map", objects: list[Object]):
        self.handlePromptAnim(delta)
        self.handleInteractions(delta)

    def handleInteractions(self, delta: int) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == NoteEnum.NOT_INTERACTING:
            self.state = NoteEnum.INTERACTING
            self.eLifted = False
        elif keys[pygame.K_e] and self.inRangeOfPlayer() and self.eLifted and self.state == NoteEnum.INTERACTING:
            self.state = NoteEnum.NOT_INTERACTING
            self.eLifted = False
        if not keys[pygame.K_e]:
            self.eLifted = True
    
    def loadPromptSprites(self) -> list[pygame.Surface]:
        sprite1 = pygame.image.load("Assets\\ShopSprites\\EkeyPrompt.png")
        sprite2 = sprite1.subsurface(pygame.Rect(11, 0, 11, 14))
        sprite1 = sprite1.subsurface(pygame.Rect(0, 0, 11, 14))
        sprite1 = pygame.transform.scale(sprite1, (22, 28))
        sprite2 = pygame.transform.scale(sprite2, (22, 28))
        return [sprite1, sprite2]
    
    def passPlayerReference(self, player) -> None:
        self.player = player
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.rect[0] + self.scaledWidth / 2
        yComponent = self.rect[1] + self.scaledHeight / 2
        return pygame.Vector2(xComponent, yComponent)

    def inRangeOfPlayer(self) -> bool:
        return (self.player.getCenter() - self.getCenter()).length() <= INTERACTABLE_DISTANCE
    
    def handlePromptAnim(self, delta: int) -> None:
        if self.inRangeOfPlayer() and self.state == NoteEnum.NOT_INTERACTING:
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
        
    def renderText(self, text: str, color: tuple[int, int, int], position: tuple[int, int], display):
        text_surface = self.fontObject.render(text, True, color)
        display.blit(text_surface, position)

    def renderTextSmall(self, text: str, color: tuple[int, int, int], position: tuple[int, int], display):
        lines = text.split('\n')
        current_y = TEXTPOS2[1]
        for line in lines:
            line_surface = self.fontObject2.render(line, True, color)
            display.blit(line_surface, (TEXTPOS2[0], current_y))
            current_y += 22

    def draw(self, display: pygame.Surface) -> None:
        if self.isPromptVisible:
            display.blit(self.promptSprites[self.currentPromptFrame], (self.rect.x + PROMPT_LOCATION[0], self.rect.y + PROMPT_LOCATION[1]))
            display.blit(self.sprite2, self.rect)
        else:
            display.blit(self.sprite1, self.rect)
        if self.state == NoteEnum.INTERACTING and self.inRangeOfPlayer():
            display.blit(self.spritemain, UIPOS)
            self.renderText("HI CHAT", (20, 20, 20), TEXTPOS, display)
            self.renderTextSmall("Okay so the way you play the game is as follows: \n - Wasd to move, space to attack \n - Go around various rooms and kill enemies for gold!!\n - You can use gold to buy potions from the 3 shops \n - Potions increase your attack :o \n... And any room can house the entrance...\n...to the final boss's lair!", (20, 20, 20), TEXTPOS2, display)
        elif self.state == NoteEnum.INTERACTING:
            self.state = NoteEnum.NOT_INTERACTING
        
