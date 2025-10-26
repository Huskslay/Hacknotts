import pygame, random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.object import Object
    from objects.enemy.enemy import Enemy
    from objects.knight import Knight

from generation.rooms.room import Room, SpriteLayer, Transition, Chest
from generation.tilemap import Tilemaps

from variables import TileEnum, TransitionDirEnum, TILE_SCALE

class CombatRoom(Room):
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

        self.room = (5, 2, 14, 8)
        layout = self.make_empty_layout()

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
        return []
    
    def make_objects(self, layout0: list[list[TileEnum]], knight: "Knight") -> list["Object"]:
        from objects.enemy.slime import Slime
        from objects.enemy.bat import Bat
        enemies: list["Object"] = []
        spawn_ranges = ((self.room[0] + 1) * TILE_SCALE, (self.room[1] + 1) * TILE_SCALE, 
                        (self.room[2] - 1) * TILE_SCALE, (self.room[3] - 1) * TILE_SCALE)
        match random.randint(0, 2):
            case 0:
                enemies: list["Object"] = [Slime(self.random_spawn_pos(spawn_ranges), knight)]
            case 1:
                enemies: list["Object"] = [Bat(self.random_spawn_pos(spawn_ranges), knight)]
            case 2:
                enemies: list["Object"] = [Slime(self.random_spawn_pos(spawn_ranges), knight), Bat(self.random_spawn_pos(spawn_ranges), knight)]
        return enemies
    def random_spawn_pos(self, spawn_ranges: tuple[int, int, int, int]) -> pygame.Vector2:
        return pygame.Vector2(random.randint(spawn_ranges[0], spawn_ranges[2]), random.randint(spawn_ranges[1], spawn_ranges[3]))
    
    def get_transitions(self, size: int, disable_transitions: list[TransitionDirEnum]) -> list[Transition]:
        transitions = [Transition(4, 5, TransitionDirEnum.LEFT, size), 
                       Transition(10, 1, TransitionDirEnum.UP, size), 
                       Transition(10, 9, TransitionDirEnum.DOWN, size),
                       Transition(15, 5, TransitionDirEnum.RIGHT, size)]
        i = 0
        while i < len(transitions):
            if transitions[i].dir in disable_transitions: transitions.pop(i)
            else: i += 1
        return transitions

    def draw(self, display: pygame.Surface) -> None:
        super().draw(display)