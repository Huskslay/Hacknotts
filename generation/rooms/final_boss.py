import pygame
from typing import TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    from objects.enemy.enemy import Enemy
    from objects.knight import Knight
    from objects.object import Object

from generation.rooms.room import Room, Transition, SpriteLayer, Tilemaps, Tilemap, Chest
from variables import TransitionDirEnum, TileEnum, TILE_SCALE, INTERACTABLE_DISTANCE, \
    ANIMATION_SPEED_PROMPT

class FinalBoss(Room):
    def __init__(self, tilemaps: Tilemaps, disable_transitions: list[TransitionDirEnum], knight: "Knight") -> None:
        super().__init__(tilemaps, disable_transitions, knight)
        
        from objects.enemy.slime import Slime
        from objects.enemy.bat import Bat
        from objects.enemy.dragon import Dragon
        
        self.phases: list[list[tuple[list[Type[Enemy]], int, int]]] = [
            [  # Phase 2
                ([Slime, Slime, Slime], 5, 5),
            ],
            [  # Phase 2
                ([Slime, Slime, Bat, Bat], 5, 5),
                ([Slime, Slime, Bat, Bat], 10, 5),
            ],
            [  # Phase 3
                ([Bat, Slime, Bat, Slime, Bat], 5, 5),
                ([Slime, Bat, Slime, Bat, Slime], 10, 5),
                ([Bat, Slime, Bat, Slime, Bat], 15, 5),
                ([Slime, Bat, Slime, Bat, Slime], 20, 5),
            ],
        ]
        self.phase = 0
        self.knight = knight
        self.dragon: Union[Dragon, None] = None

        self.summon_next_phase()
        
        
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

        room = (1, 2, 18, 8)
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
    
    def make_objects(self, layout0: list[list[TileEnum]], knight: "Knight") -> list["Object"]:
        return []
    
    def get_transitions(self, size: int, disable_transitions: list[TransitionDirEnum]) -> list[Transition]:
        transitions = []
        i = 0
        while i < len(transitions):
            if transitions[i].dir in disable_transitions: transitions.pop(i)
            else: i += 1
        return transitions

    def summon_next_phase(self) -> None:
        if self.phase >= len(self.phases): 
            self.summon_boss()
            return

        summoners = self.phases[self.phase]
        self.phase += 1

        from objects.enemy.enemy_summoner import EnemySummoner
        for summon in summoners:
            sum = EnemySummoner(pygame.Vector2(
                summon[1] * TILE_SCALE, summon[2] * TILE_SCALE), self.knight)
            sum.go(self, summon[0])
            self.objects.append(sum)

    def summon_boss(self) -> None:
        from objects.enemy.dragon import Dragon
        self.dragon = Dragon(pygame.Vector2(10 * TILE_SCALE, 5 * TILE_SCALE), self.knight)
        self.objects.append(self.dragon)


    def draw(self, display: pygame.Surface) -> None:   

        if self.dragon != None:
            if not self.dragon.alive:
                print("Dragon defeated!")
        else:
            from objects.enemy.enemy import Enemy 
            i = 0
            passed = True
            while i < len(self.objects):
                object = self.objects[i]
                if isinstance(object, Enemy):
                    if not object.alive:
                        self.objects.pop(i)
                    else: 
                        passed = False
                        i += 1
            if passed: self.summon_next_phase()

        super().draw(display)