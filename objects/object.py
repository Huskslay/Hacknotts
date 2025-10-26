import pygame

from generation.map import Map

class Object:
    def __init__(self) -> None:
        self.hitbox_offset = (0, 0)

    def update(self, delta: int, map: Map, objects: list["Object"]) -> None:
        self.hitbox : pygame.Rect
        self.hitboxSize : tuple[int, int]
        self.pos : pygame.Vector2
        self.size : tuple[int, int]

    def move_by(self, x: float, y: float, map: Map, force: bool = False) -> None:
        self.move_to(self.pos.x + x, self.pos.y + y, map, force)

    def move_to(self, x: float, y: float, map: Map, force: bool = False) -> None:
        old_pos = self.pos
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2) + \
            self.hitbox_offset[0]
        self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2) + \
            self.hitbox_offset[1]

        if force: return

        if map.get_room().is_colliding(self.hitbox):
            self.pos = pygame.Vector2(x, old_pos.y)
            self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
            self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)
            if map.get_room().is_colliding(self.hitbox):
                self.pos = pygame.Vector2(old_pos.x, y)
                self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
                self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)
                if map.get_room().is_colliding(self.hitbox):
                    self.pos = old_pos
                    self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
                    self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)

    def move_to_force(self, x: float, y: float) -> None:
        self.pos = pygame.Vector2(x, y)
        self.hitbox.x = (int)(self.pos.x + self.size[0] / 2 - self.hitboxSize[0] / 2)
        self.hitbox.y = (int)(self.pos.y + self.size[1] / 2 - self.hitboxSize[1] / 2)


    def draw(self, display: pygame.Surface) -> None:
        pass 