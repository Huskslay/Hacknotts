import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.enemy.enemy import Enemy
    from objects.knight import Knight

from generation.rooms.room import Room, Transition, SpriteLayer, Tilemaps, Tilemap, Chest
from variables import TransitionDirEnum, TileEnum, TILE_SCALE, INTERACTABLE_DISTANCE, \
    ANIMATION_SPEED_PROMPT

PROMPT_LOCATION = (50, -18)

class FinalHallway(Room):
    def __init__(self, tilemaps: Tilemaps, disable_transitions: list[TransitionDirEnum], knight: "Knight") -> None:
        super().__init__(tilemaps, disable_transitions, knight)
        self.hole = Hole(18, 5, TILE_SCALE, tilemaps.get_map("hole"), knight)
        self.laddder = Ladder(1, 5, TILE_SCALE, tilemaps.get_map("ladder"), knight)
        
        
    def make_empty_layout(self) -> list[list[list[TileEnum]]]:
        layout: list[list[list[TileEnum]]] = []
        for i in range(len(self.sprite_layers)):
            layout.append([])
            for y in range(len(self.sprite_layers[i].tiles)):
                layout[-1].append([])
                for x in range(len(self.sprite_layers[i].tiles[0])):
                    layout[-1][-1].append(TileEnum.EMPTY)
        return layout

    def make_layout(self, tilemaps: Tilemaps) -> list[list[list[TileEnum]]]:
        self.sprite_layers = [SpriteLayer(tilemaps.get_map("dungeon"))]

        room = (1, 4, 18, 6)
        layout = self.make_empty_layout()

        for x in range(room[0], room[2] + 1):
            for y in range(room[1], room[3] + 1):
                if x == room[0] and y == room[1]: 
                    layout[0][y][x] = TileEnum.TL
                elif x == room[2] and y == room[1]: 
                    layout[0][y][x] = TileEnum.TR
                elif x == room[0] and y == room[3]: 
                    layout[0][y][x] = TileEnum.BL
                elif x == room[2] and y == room[3]: 
                    layout[0][y][x] = TileEnum.BR
                else: layout[0][y][x] = TileEnum.FLOOR

        return layout
    
    def make_chests(self, size: int) -> list["Chest"]:
        return []
    
    def get_transitions(self, size: int, disable_transitions: list[TransitionDirEnum]) -> list[Transition]:
        transitions = []
        i = 0
        while i < len(transitions):
            if transitions[i].dir in disable_transitions: transitions.pop(i)
            else: i += 1
        return transitions

    def draw(self, display: pygame.Surface) -> None:
        super().draw(display)
        self.hole.draw(display)
        self.laddder.draw(display)


class Hole:
    def __init__(self, x: int, y: int, size: int, tilemap: Tilemap, player: "Knight") -> None:
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.tilemap = tilemap
        self.promptSprites = self.loadPromptSprites()
        self.promptTimer = ANIMATION_SPEED_PROMPT
        self.currentPromptFrame = 0
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] * TILE_SCALE + TILE_SCALE / 2
        yComponent = self.pos[1] * TILE_SCALE + TILE_SCALE / 2
        return pygame.Vector2(xComponent, yComponent)

    def inRangeOfPlayer(self) -> bool:
        return (self.player.getCenter() - self.getCenter()).length() <= INTERACTABLE_DISTANCE

    def loadPromptSprites(self) -> list[pygame.Surface]:
        sprite1 = pygame.image.load("Assets\\ShopSprites\\EkeyPrompt.png")
        sprite2 = sprite1.subsurface(pygame.Rect(11, 0, 11, 14))
        sprite1 = sprite1.subsurface(pygame.Rect(0, 0, 11, 14))
        sprite1 = pygame.transform.scale(sprite1, (22, 28))
        sprite2 = pygame.transform.scale(sprite2, (22, 28))
        return [sprite1, sprite2]

    def handlePromptAnim(self, delta: int) -> None:
        if self.inRangeOfPlayer():
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

    def draw(self, display: pygame.Surface) -> None:
        self.handlePromptAnim(1)

        if self.inRangeOfPlayer(): image = 1
        else: image = 0
        display.blit(self.tilemap.tiles[image], (self.pos.x * TILE_SCALE, self.pos.y * TILE_SCALE))
        if image == 1: 
            display.blit(self.promptSprites[self.currentPromptFrame], (self.pos.x * TILE_SCALE + PROMPT_LOCATION[0], self.pos.y * TILE_SCALE + PROMPT_LOCATION[1]))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and image == 1:
            self.player.to_final_boss = True



class Ladder:
    def __init__(self, x: int, y: int, size: int, tilemap: Tilemap, player: "Knight") -> None:
        self.pos = pygame.Vector2(x, y)
        self.player = player
        self.tilemap = tilemap
        self.promptSprites = self.loadPromptSprites()
        self.promptTimer = ANIMATION_SPEED_PROMPT
        self.currentPromptFrame = 0
    
    def getCenter(self) -> pygame.Vector2:
        xComponent = self.pos[0] * TILE_SCALE + TILE_SCALE / 2
        yComponent = self.pos[1] * TILE_SCALE + TILE_SCALE / 2
        return pygame.Vector2(xComponent, yComponent)

    def inRangeOfPlayer(self) -> bool:
        return (self.player.getCenter() - self.getCenter()).length() <= INTERACTABLE_DISTANCE

    def loadPromptSprites(self) -> list[pygame.Surface]:
        sprite1 = pygame.image.load("Assets\\ShopSprites\\EkeyPrompt.png")
        sprite2 = sprite1.subsurface(pygame.Rect(11, 0, 11, 14))
        sprite1 = sprite1.subsurface(pygame.Rect(0, 0, 11, 14))
        sprite1 = pygame.transform.scale(sprite1, (22, 28))
        sprite2 = pygame.transform.scale(sprite2, (22, 28))
        return [sprite1, sprite2]

    def handlePromptAnim(self, delta: int) -> None:
        if self.inRangeOfPlayer():
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

    def draw(self, display: pygame.Surface) -> None:
        self.handlePromptAnim(1)

        if self.inRangeOfPlayer(): image = 1
        else: image = 0
        display.blit(self.tilemap.tiles[image], (self.pos.x * TILE_SCALE, self.pos.y * TILE_SCALE))
        if image == 1: 
            display.blit(self.promptSprites[self.currentPromptFrame], (self.pos.x * TILE_SCALE + PROMPT_LOCATION[0], self.pos.y * TILE_SCALE + PROMPT_LOCATION[1]))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and image == 1:
            self.player.quit_final_hallway = True