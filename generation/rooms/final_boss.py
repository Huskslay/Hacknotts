import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.enemy.enemy import Enemy
    from objects.knight import Knight

from generation.rooms.room import Room, Transition, SpriteLayer, Tilemaps, Tilemap, Chest
from variables import TransitionDirEnum, TileEnum, TILE_SCALE, INTERACTABLE_DISTANCE, \
    ANIMATION_SPEED_PROMPT

class FinalBoss(Room):
    def __init__(self, tilemaps: Tilemaps, disable_transitions: list[TransitionDirEnum], knight: "Knight") -> None:
        super().__init__(tilemaps, disable_transitions, knight)
        
        
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