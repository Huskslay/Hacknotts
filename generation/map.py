import pygame
from random import randint

from generation.rooms.start_room import Room, StartRoom
from generation.rooms.combat_room import CombatRoom
from generation.rooms.chest_room import ChestRoom
from generation.tilemap import Tilemaps

from variables import ROOM_SIZE, TransitionDirEnum, TILE_SCALE, CHEST_ROOMS


class Map:
    def __init__(self, tilemaps: Tilemaps) -> None:  
        self.rooms: list[list[Room]] = []

        chest_rooms: list[tuple[int, int]] = []
        while len(chest_rooms) < CHEST_ROOMS:
            pos = (randint(0, ROOM_SIZE[0]), randint(0, ROOM_SIZE[1]))
            if pos[0] == ROOM_SIZE[1] // 2 and pos[1] == ROOM_SIZE[0] // 2 or \
                pos in self.rooms: continue 
            chest_rooms.append(pos)


        for y in range(ROOM_SIZE[1]):
            self.rooms.append([])
            for x in range(ROOM_SIZE[0]):
                disable_transitions: list[TransitionDirEnum] = []
                if x == ROOM_SIZE[0] - 1: disable_transitions.append(TransitionDirEnum.DOWN)
                if x == 0: disable_transitions.append(TransitionDirEnum.UP)
                if y == ROOM_SIZE[1] - 1: disable_transitions.append(TransitionDirEnum.RIGHT)
                if y == 0: disable_transitions.append(TransitionDirEnum.LEFT)

                if (x, y) in chest_rooms: 
                    # if TransitionDirEnum.UP not in disable_transitions:
                    #     disable_transitions.append(TransitionDirEnum.UP)
                    self.rooms[-1].append(ChestRoom(tilemaps, disable_transitions))
                else: self.rooms[-1].append(CombatRoom(tilemaps, disable_transitions))

        self.rooms[ROOM_SIZE[1] // 2][ROOM_SIZE[0] // 2] = StartRoom(tilemaps, [])
        self.room = (ROOM_SIZE[1] // 2, ROOM_SIZE[0] // 2)

    def get_room(self) -> Room:
        return self.rooms[self.room[0]][self.room[1]]

    def transition(self, transitionDir: TransitionDirEnum, knight) -> None:
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

    def draw(self, display: pygame.Surface) -> None:
        self.get_room().draw(display)