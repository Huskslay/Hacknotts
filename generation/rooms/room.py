import pygame
from random import randint

from generation.tilemap import Tilemaps, Tilemap
from variables import SIZE, TileEnum, TILE_SCALE

class Room:
    def __init__(self, tilemaps: Tilemaps) -> None:
        self.sprite_layers: list[SpriteLayer] = []
        self.layers: list[Layer] = []
        self.generate(tilemaps)

    def generate(self, tilemaps: Tilemaps) -> None:
        layout = self.make_layout(tilemaps)
        self.generate_sprite_layers(layout)
        self.generate_transition_layer(self.get_transitions(), tilemaps)
        self.generate_collision_layer(layout)
        
        for layer in self.sprite_layers:
            self.layers.append(layer)
        self.layers.append(self.transition_layer)
        

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

    def generate_transition_layer(self, transitions: list[tuple[int, int]], tilemaps: Tilemaps) -> None:
        self.transition_layer = TransitionLayer(tilemaps.get_map("transition"))
        self.transition_layer.tiles = transitions

    def generate_collision_layer(self, layout: list[list[list[TileEnum]]]) -> None:
        layout0 = layout[0]
        self.rects: list[pygame.Rect] = []
        for x in range(len(layout0[0])):
            for y in range(len(layout0)):
                if layout0[y][x] == TileEnum.EMPTY and (x, y) not in self.transition_layer.tiles:
                    self.rects.append(
                        pygame.Rect(x * TILE_SCALE, y * TILE_SCALE, TILE_SCALE, TILE_SCALE)
                    )
        pass

    def is_colliding(self, hitbox : pygame.Rect) -> bool:
        for i in range(len(self.rects)):
            if self.rects[i].colliderect(hitbox): return True
        return False

    def make_layout(self, tilemaps: Tilemaps) -> list[list[list[TileEnum]]]:
        return []
    
    def get_transitions(self) -> list[tuple[int, int]]:
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
        self.tiles: list[tuple[int, int]] = []

    def draw(self, display: pygame.Surface) -> None:
        for tile in self.tiles:
            display.blit(self.tilemap.tiles[0], 
                        pygame.Vector2(tile[0] * self.tilemap.size, tile[1] * self.tilemap.size))

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
                
class CollisiionLayer(Layer):
    def __init__(self, tilemap: Tilemap) -> None:
        super().__init__(tilemap)


    def draw(self, display: pygame.Surface) -> None:
        pass