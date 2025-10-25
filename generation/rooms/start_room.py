import pygame

from generation.rooms.room import Room, SpriteLayer
from generation.tilemap import Tilemaps

from variables import TileEnum

class StartRoom(Room):
    def __init__(self, tilemaps: Tilemaps) -> None:
        super().__init__(tilemaps)
        
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
        
        room = (4, 4, 12, 8)
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
    
    def get_transitions(self) -> list[tuple[int, int]]:
        return [(0, 0), (0, 1), (0, 2), (1, 0)]

    def draw(self, display: pygame.Surface) -> None:
        super().draw(display)