import pygame
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.enemy import Enemy
    from objects.knight import Knight

from generation.tilemap import Tilemaps, Tilemap
from variables import SIZE, TileEnum, TILE_SCALE, TransitionDirEnum

class Room:
    def __init__(self, tilemaps: Tilemaps, disable_transitions: list[TransitionDirEnum], knight: "Knight") -> None:
        self.sprite_layers: list[SpriteLayer] = []
        self.layers: list[Layer] = []
        self.chests: list[Chest] = []
        
        layout = self.make_layout(tilemaps)
        chests = self.make_chests(TILE_SCALE)
        self.enemies = self.make_enemies(layout[0], knight)

        self.generate_sprite_layers(layout)
        self.generate_transition_layer(self.get_transitions(TILE_SCALE, disable_transitions), tilemaps)
        self.generate_chests_layer(chests, tilemaps)
        self.generate_collision(layout)
        
        for layer in self.sprite_layers:
            self.layers.append(layer)
        self.layers.append(self.transition_layer)
        self.layers.append(self.chests_layer)
        

    def generate_sprite_layers(self, layout: list[list[list[TileEnum]]]) -> None:
        for i in range(len(self.sprite_layers)):
            for x in range(len(self.sprite_layers[i].tiles[0])):
                for y in range(len(self.sprite_layers[i].tiles)):
                    self.generate_tile(x, y, i, layout)

    def generate_tile(self, x: int, y: int, i: int, layout: list[list[list[TileEnum]]]) -> None:
        match (layout[i][y][x]):
            case TileEnum.TL:
                self.sprite_layers[i].tiles[y][x] = self.sprite_layers[i].tilemap.tls[
                            randint(0, len(self.sprite_layers[i].tilemap.tls) - 1)
                ]
            case TileEnum.TR:
                self.sprite_layers[i].tiles[y][x] = self.sprite_layers[i].tilemap.trs[
                            randint(0, len(self.sprite_layers[i].tilemap.trs) - 1)
                ]
            case TileEnum.BL:
                self.sprite_layers[i].tiles[y][x] = self.sprite_layers[i].tilemap.bls[
                            randint(0, len(self.sprite_layers[i].tilemap.bls) - 1)
                ]
            case TileEnum.BR:
                self.sprite_layers[i].tiles[y][x] = self.sprite_layers[i].tilemap.brs[
                            randint(0, len(self.sprite_layers[i].tilemap.brs) - 1)
                ]
            case TileEnum.FLOOR:
                self.sprite_layers[i].tiles[y][x] = self.sprite_layers[i].tilemap.floors[
                            randint(0, len(self.sprite_layers[i].tilemap.floors) - 1)
                ]
            case _:
                pass

    def generate_transition_layer(self, transitions: list["Transition"], tilemaps: Tilemaps) -> None:
        self.transition_layer = TransitionLayer(tilemaps.get_map("transition"))
        self.transition_layer.transitions = transitions

    def generate_chests_layer(self, chests: list["Chest"], tilemaps: Tilemaps) -> None:
        self.chests_layer = ChestsLayer(tilemaps.get_map("chests"))
        self.chests_layer.chests = chests

    def generate_collision(self, layout: list[list[list[TileEnum]]]) -> None:
        layout0 = layout[0]
        self.collision_rects: list[pygame.Rect] = []
        for x in range(len(layout0[0])):
            for y in range(len(layout0)):
                if self.is_non_empty(layout0, x, y) and self.is_adjacent_to_non_empty(layout0, x, y):
                    self.collision_rects.append(
                        pygame.Rect(x * TILE_SCALE, y * TILE_SCALE, TILE_SCALE, TILE_SCALE)
                    )

    def is_adjacent_to_non_empty(self, layout0: list[list[TileEnum]], x, y) -> bool:
        return (x > 0 and not self.is_non_empty(layout0, x - 1, y)) or \
               (x < len(layout0[0]) - 1 and not self.is_non_empty(layout0, x + 1, y)) or \
               (y > 0 and not self.is_non_empty(layout0, x, y - 1)) or \
               (y < len(layout0) - 1 and not self.is_non_empty(layout0, x, y + 1))
    def is_non_empty(self, layout0: list[list[TileEnum]], x, y) -> bool:
        return layout0[y][x] == TileEnum.EMPTY and not self.transition_layer.transition_at_point(x, y)

    def is_colliding(self, hitbox : pygame.Rect) -> bool:
        for i in range(len(self.collision_rects)):
            if self.collision_rects[i].colliderect(hitbox): return True
        return False

    def make_layout(self, tilemaps: Tilemaps) -> list[list[list[TileEnum]]]:
        return []
    
    def make_chests(self, size: int) -> list["Chest"]:
        return []
    
    def make_enemies(self, layout0: list[list[TileEnum]], knight: "Knight") -> list["Enemy"]:
        return []

    def get_transitions(self, size: int, disable_transitions: list[TransitionDirEnum]) -> list["Transition"]:
        return []

    def draw(self, display: pygame.Surface) -> None:
        for i in range(len(self.layers)):
            self.layers[i].draw(display)


class Layer:
    def __init__(self, tilemap: Tilemap) -> None:
        self.tilemap = tilemap
        pass

    def draw(self, display: pygame.Surface) -> None:
        pass
                
class TransitionLayer(Layer):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__(tilemap)
        self.transitions: list[Transition] = []

    def transition_at_point(self, x: int, y: int) -> bool:
        for transition in self.transitions:
            if transition.pos.x == x and transition.pos.y == y: return True
        return False

    def transition_at_dir(self, dir: TransitionDirEnum) -> "Transition":
        for transition in self.transitions:
            if transition.dir == dir: return transition
        return self.transitions[0]

    def draw(self, display: pygame.Surface) -> None:
        for transition in self.transitions:
            display.blit(self.tilemap.tiles[transition.get_sprite()], 
                        pygame.Vector2(transition.pos[0] * self.tilemap.size, transition.pos[1] * self.tilemap.size))

class Transition:
    def __init__(self, x: int, y: int, dir: TransitionDirEnum, size: int) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(self.pos.x * size, self.pos.y * size, size, size)
        self.dir = dir

    def get_sprite(self) -> int:
        return 0


class ChestsLayer(Layer):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__(tilemap)
        self.chests: list[Chest] = []

    def draw(self, display: pygame.Surface) -> None:
        for chest in self.chests:
            display.blit(self.tilemap.tiles[chest.get_sprite()], 
                        pygame.Vector2(chest.pos.x * self.tilemap.size, chest.pos.y * self.tilemap.size))

class Chest:
    def __init__(self, x: int, y: int, size: int) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(self.pos.x * size, self.pos.y * size, size, size)
        self.opened = False

    def get_sprite(self) -> int:
        if self.opened: return 1
        return 0

class SpriteLayer(Layer):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__(tilemap)
        self.tiles: list[list[int]] = []
        for y in range(SIZE[1] // self.tilemap.size):
            self.tiles.append([])
            for x in range(SIZE[0] // self.tilemap.size):
                self.tiles[-1].append(-1)

    def draw(self, display: pygame.Surface) -> None:
        for x in range(len(self.tiles[0])):
            for y in range(len(self.tiles)):
                # empty
                if self.tiles[y][x] == -1:
                    continue
                # issue
                if self.tiles[y][x] < -1 or self.tiles[y][x] >= len(self.tilemap.tiles): 
                    print(f"Index for tile of {self.tiles[y][x]} out of range")
                    continue
                # normal
                display.blit(self.tilemap.tiles[self.tiles[y][x]], 
                             pygame.Vector2(x * self.tilemap.size, y * self.tilemap.size))