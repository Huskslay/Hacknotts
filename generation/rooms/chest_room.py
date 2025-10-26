import pygame
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.enemy.enemy import Enemy
    from objects.knight import Knight

from generation.rooms.room import Room, SpriteLayer, Transition, Chest
from generation.tilemap import Tilemaps

from variables import TileEnum, TransitionDirEnum, TRY_SPAWN_CHESTS

class ChestRoom(Room):
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
        self.sprite_layers = [SpriteLayer(tilemaps.get_map("grass"))]

        layout = self.make_empty_layout()
        self.room = (7, 3, 12, 6)

        for x in range(self.room[0], self.room[2] + 1):
            for y in range(self.room[1], self.room[3] + 1):
                if x == self.room[0] and y == self.room[1]: 
                    layout[0][y][x] = TileEnum.TL
                elif x == self.room[2] and y == self.room[1]: 
                    layout[0][y][x] = TileEnum.TR
                elif x == self.room[0] and y == self.room[3]: 
                    layout[0][y][x] = TileEnum.BL
                elif x == self.room[2] and y == self.room[3]: 
                    layout[0][y][x] = TileEnum.BR
                else: layout[0][y][x] = TileEnum.FLOOR

        return layout
    
    def make_chests(self, size: int) -> list["Chest"]:
        made_chests: list[tuple[int, int]] = []
        chests: list[Chest] = []
        for _ in range(TRY_SPAWN_CHESTS):
            pos = (randint(self.room[0], self.room[2]), randint(self.room[1], self.room[3]))
            if pos in made_chests or pos[0] == self.room[0] or pos[1] == self.room[1] or \
               pos[0] == self.room[2] or pos[1] == self.room[3]: continue
            made_chests.append(pos)
            chests.append(Chest(pos[0], pos[1], size))
        return chests
    
    def get_transitions(self, size: int, disable_transitions: list[TransitionDirEnum]) -> list[Transition]:
        transitions = [Transition(6, 5, TransitionDirEnum.LEFT, size), 
                       Transition(10, 2, TransitionDirEnum.UP, size), 
                       Transition(10, 7, TransitionDirEnum.DOWN, size),
                       Transition(13, 5, TransitionDirEnum.RIGHT, size)]
        i = 0
        while i < len(transitions):
            if transitions[i].dir in disable_transitions: transitions.pop(i)
            else: i += 1
        return transitions

    def draw(self, display: pygame.Surface) -> None:
        super().draw(display)