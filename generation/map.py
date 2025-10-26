import pygame
from random import randint, randrange
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.knight import Knight

from generation.rooms.start_room import Room, StartRoom
from generation.rooms.combat_room import CombatRoom
from generation.rooms.chest_room import ChestRoom
from generation.rooms.shopkeepers_room import ShopkeepersRoom
from generation.rooms.boss_entry_room import BossEntryRoom
from generation.rooms.final_hallway import FinalHallway
from generation.rooms.final_boss import FinalBoss

from generation.tilemap import Tilemaps

from variables import MAP_SIZE, TransitionDirEnum, TILE_SCALE, CHEST_ROOMS, SHOPKEEPER_ROOMS

FINALHALLWAY = (-1, -1)
FINALHALLWAY_POS = (2.5, 5)
FINALBOSS = (-2, -2)
FINALBOSS_POS = (10, 5)

class Map:
    def __init__(self, tilemaps: Tilemaps, knight: "Knight") -> None:  
        self.rooms: list[list[Room]] = []

        self.final_hallway = FinalHallway(tilemaps, [], knight)
        self.final_boss = FinalBoss(tilemaps, [], knight)

        self.boss_entry_room = self.random_edge_coord(MAP_SIZE)
        chest_rooms: list[tuple[int, int]] = []
        while len(chest_rooms) < CHEST_ROOMS:
            pos = (randint(0, MAP_SIZE), randint(0, MAP_SIZE))
            if pos[0] == MAP_SIZE // 2 and pos[1] == MAP_SIZE // 2 or \
                pos == self.boss_entry_room or pos in self.rooms: continue 
            chest_rooms.append(pos)
        shopkeeper_rooms: list[tuple[int, int]] = []
        while len(shopkeeper_rooms) < SHOPKEEPER_ROOMS:
            pos = (randint(0, MAP_SIZE), randint(0, MAP_SIZE))
            if pos[0] == MAP_SIZE // 2 and pos[1] == MAP_SIZE // 2 or \
               pos == self.boss_entry_room or pos in self.rooms or pos in chest_rooms: continue
            shopkeeper_rooms.append(pos)

        for y in range(MAP_SIZE):
            self.rooms.append([])
            for x in range(MAP_SIZE):
                disable_transitions: list[TransitionDirEnum] = []
                if x == MAP_SIZE - 1: disable_transitions.append(TransitionDirEnum.DOWN)
                if x == 0: disable_transitions.append(TransitionDirEnum.UP)
                if y == MAP_SIZE - 1: disable_transitions.append(TransitionDirEnum.RIGHT)
                if y == 0: disable_transitions.append(TransitionDirEnum.LEFT)

                if (x, y) == self.boss_entry_room: 
                    self.rooms[-1].append(BossEntryRoom(tilemaps, disable_transitions, knight))
                elif (x, y) in chest_rooms: 
                    if TransitionDirEnum.UP not in disable_transitions:
                        disable_transitions.append(TransitionDirEnum.UP)
                    self.rooms[-1].append(ChestRoom(tilemaps, disable_transitions, knight))
                elif (x, y) in shopkeeper_rooms: 
                    if TransitionDirEnum.DOWN not in disable_transitions:
                        disable_transitions.append(TransitionDirEnum.DOWN)
                    self.rooms[-1].append(ShopkeepersRoom(tilemaps, disable_transitions, knight))
                else: self.rooms[-1].append(CombatRoom(tilemaps, disable_transitions, knight))

        self.rooms[MAP_SIZE // 2][MAP_SIZE // 2] = BossEntryRoom(tilemaps, [], knight)
        self.room = (MAP_SIZE // 2, MAP_SIZE // 2)

    def random_edge_coord(self, width: int = 10) -> tuple[int, int]:
        if width <= 1:
            return (0, 0)
        perimeter = 4 * width - 4
        rand = randrange(perimeter)
        if rand < width:
            return (rand, 0)
        rand -= width
        if rand < width - 2:
            return (width - 1, 1 + rand)
        rand -= (width - 2)
        if rand < width:
            return ((width - 1) - rand, width - 1)
        rand -= width
        return (0, (width - 2) - rand)

    def get_room(self) -> Room:
        if self.room == FINALHALLWAY: return self.final_hallway
        if self.room == FINALBOSS: return self.final_boss
        return self.rooms[self.room[0]][self.room[1]]

    def transition(self, transitionDir: TransitionDirEnum, knight: "Knight") -> None:
        
        match (transitionDir):
            case TransitionDirEnum.LEFT:
                self.room = (self.room[0] - 1, self.room[1])
                pos = self.get_room().transition_layer.transition_at_dir(TransitionDirEnum.RIGHT).pos
                knight.move_to_force(pos.x * TILE_SCALE - TILE_SCALE, pos.y * TILE_SCALE)
            case TransitionDirEnum.UP: 
                self.room = (self.room[0], self.room[1] - 1)
                pos = self.get_room().transition_layer.transition_at_dir(TransitionDirEnum.DOWN).pos
                knight.move_to_force(pos.x * TILE_SCALE, pos.y * TILE_SCALE - TILE_SCALE)
            case TransitionDirEnum.DOWN:
                self.room = (self.room[0], self.room[1] + 1)
                pos = self.get_room().transition_layer.transition_at_dir(TransitionDirEnum.UP).pos
                knight.move_to_force(pos.x * TILE_SCALE, pos.y * TILE_SCALE + TILE_SCALE)
            case TransitionDirEnum.RIGHT: 
                self.room = (self.room[0] + 1, self.room[1])
                pos = self.get_room().transition_layer.transition_at_dir(TransitionDirEnum.LEFT).pos
                knight.move_to_force(pos.x * TILE_SCALE + TILE_SCALE, pos.y * TILE_SCALE)

    def transition_to_final_hallway(self, knight: "Knight") -> None:
        self.room = FINALHALLWAY
        knight.move_to_force(FINALHALLWAY_POS[0] * TILE_SCALE, FINALHALLWAY_POS[1] * TILE_SCALE)

    def quit_final_hallway(self, knight: "Knight") -> None:
        self.room = (self.boss_entry_room[1], self.boss_entry_room[0])
        room = self.get_room()
        if isinstance(room, BossEntryRoom):
            pos = room.trapdoor.pos
        else:
            pos = room.transition_layer.transition_at_dir(TransitionDirEnum.LEFT).pos \
                    + pygame.Vector2(1, 0)
        knight.move_to_force(pos.x * TILE_SCALE, pos.y * TILE_SCALE + TILE_SCALE)

    def transition_to_final_boss(self, knight: "Knight") -> None:
        self.room = FINALBOSS
        knight.move_to_force(FINALBOSS_POS[0] * TILE_SCALE, FINALBOSS_POS[1] * TILE_SCALE)

    def draw(self, display: pygame.Surface) -> None:
        self.get_room().draw(display)