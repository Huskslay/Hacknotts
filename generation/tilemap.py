import pygame
from variables import BG_SCALE, TileEnum

class Tilemap:
    def __init__(self, path: str, size: int, tiles: list[list[TileEnum]]) -> None:
        self.size = size
        self.sheet = pygame.image.load(path).convert_alpha()
        self.sheet = pygame.transform.scale(self.sheet, 
                    (self.sheet.get_width() * BG_SCALE, self.sheet.get_height() * BG_SCALE))
        self.tiles: list[pygame.Surface] = []
        self.floors: list[int] = []
        self.tls: list[int] = []
        self.trs: list[int] = []
        self.bls: list[int] = []
        self.brs: list[int] = []
     
        for x in range(len(tiles[0])):
            for y in range(len(tiles)):
                match (tiles[y][x]):
                    case TileEnum.FLOOR:
                        self.floors.append(len(self.tiles))
                        self.tiles.append(
                            self.sheet.subsurface(
                                pygame.Rect(x * size, y * size, size, size))
                        )
                    case TileEnum.TL:
                        self.tls.append(len(self.tiles))
                        self.tiles.append(
                            self.sheet.subsurface(
                                pygame.Rect(x * size, y * size, size, size))
                        )
                        self.bls.append(len(self.tiles))
                        self.tiles.append(
                            pygame.transform.flip(self.sheet.subsurface(
                                pygame.Rect(x * size, y * size, size, size)), 0, 1)
                        )
                    case TileEnum.TR:
                        self.trs.append(len(self.tiles))
                        self.tiles.append(
                            self.sheet.subsurface(
                                pygame.Rect(x * size, y * size, size, size))
                        )
                        self.brs.append(len(self.tiles))
                        self.tiles.append(
                            pygame.transform.flip(self.sheet.subsurface(
                                pygame.Rect(x * size, y * size, size, size)), 0, 1)
                        )

class Tilemaps:
    def __init__(self) -> None:
        self.tilemaps: dict[str, Tilemap] = {}

    def add_tilemap(self, name: str, path: str, size: int, tiles: list[list[TileEnum]]) -> None:
       self.tilemaps[name] = Tilemap(path, size, tiles)

    def get_map(self, name: str) -> Tilemap:
        return self.tilemaps[name]