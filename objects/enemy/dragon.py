import pygame
from enum import Enum
from typing import TYPE_CHECKING, Union
import random

if TYPE_CHECKING:
    from objects.knight import Knight

from objects.object import Object
from generation.map import Map
from objects.enemy.enemy import Enemy, EnemyStateEnum, DirectionEnum, Projectile
from objects.coin import Coin

from variables import TILE_SCALE, SIZE

ANIMSPEED = 220 ## Wait time in ms between sprite changes in anim

UP_F1 = 0
RIGHT_F1 = 3
DOWN_F1 = 7
LEFT_F1 = 11
FRAMES = 3
SPEED = 0.25
HEALTH = 50
RECOIL_AMOUNT = 0
FLY = 4500
MOB_SUM = 20000

XSPRITES = 3
YSPRITES = 4

class Dragon(Enemy):
    def __init__(self, pos: pygame.Vector2, knight: Union["Knight", None] = None) -> None:
        from generation.rooms.room import Room
        self.room: Union[Room, None] = None
        self.spriteChangeWaitTimer = ANIMSPEED
        super().__init__(pos, knight)
        self.spriteSize = (191, 161)
        self.size = (191, 161)
        self.hitboxSize = (191, 161)
        self.hitbox_offset = (191 // 2, 161 // 2)
        self.hitbox = pygame.Rect(1, 1, self.hitboxSize[0], self.hitboxSize[1])
        self.move_to_force(pos.x, pos.y)
        self.initialiseSprites("Assets\\Dwagon.png", XSPRITES, YSPRITES, self.spriteSize)
        self.health = HEALTH
        self.recoilAmount = RECOIL_AMOUNT
        self.directionFacing = DirectionEnum.DOWN
        self.progress = FLY
        self.mob_counter = MOB_SUM
        self.hit_player = False

    def initialiseSprites(self, spritesheetPath: str, xSprites: int, ySprites: int, spriteSize: tuple[int, int]) -> None:
        self.spritesheet = pygame.image.load(spritesheetPath).convert_alpha()
        self.up = [
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(0, 0, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191, 0, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191*2, 0, 191, 161)),
                (191 * 2, 161 * 2)
            )
        ]
        self.right = [
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(0, 161, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191, 161, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191*2, 161, 191, 161)),
                (191 * 2, 161 * 2)
            )
        ]
        self.down = [
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(0, 161*2, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191, 161*2, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191*2, 161*2, 191, 161)),
                (191 * 2, 161 * 2)
            )
        ]
        self.left = [
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(0, 161*3, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191, 161*3, 191, 161)),
                (191 * 2, 161 * 2)
            ),
            pygame.transform.scale(
                self.spritesheet.subsurface(pygame.Rect(191*2, 161*3, 191, 161)),
                (191 * 2, 161 * 2)
            )
        ]
    
    def setSpriteGivenDirection(self, sprites: list[pygame.Surface]) -> None:
        if self.spriteChangeWaitTimer <= 0:
            self.spriteChangeWaitTimer = ANIMSPEED
            self.currentSprite += 1
            if self.currentSprite >= 3: 
                self.currentSprite = 0
        self.sprite = sprites[self.currentSprite]
    
    def update(self, delta, map: Map, objects: list[Object]) -> None:
        self.spriteChangeWaitTimer -= delta

        if self.directionFacing == DirectionEnum.UP:
            self.setSpriteGivenDirection(self.up)
        elif self.directionFacing == DirectionEnum.LEFT:
            self.setSpriteGivenDirection(self.left)
        elif self.directionFacing == DirectionEnum.RIGHT:
            self.setSpriteGivenDirection(self.right)
        else: self.setSpriteGivenDirection(self.down)
        super().update(delta, map, objects)

        if self.directionFacing == DirectionEnum.UP:
            self.move_by(0, -SPEED * delta, map, True)
        elif self.directionFacing == DirectionEnum.DOWN:
            self.move_by(0, SPEED * delta, map, True)
        elif self.directionFacing == DirectionEnum.LEFT:
            self.move_by(-SPEED * delta, 0, map, True)
        elif self.directionFacing == DirectionEnum.RIGHT:
            self.move_by(SPEED * delta, 0, map, True)
        

        self.mob_counter -= delta
        if self.mob_counter <= 0:
            self.mob_counter = MOB_SUM 
            if self.room != None:
                from objects.enemy.enemy_summoner import EnemySummoner
                from objects.enemy.slime import Slime
                from objects.enemy.bat import Bat
                x = random.randint(2, 16)
                y = random.randint(3, 7)
                sum = EnemySummoner(pygame.Vector2(
                    x * TILE_SCALE, y * TILE_SCALE), self.player)
                sum.go(self.room, random.choice([[Bat],[Slime]]))
                self.room.objects.append(sum)

            
        self.progress -= delta
        if self.progress <= 0: 
            self.hit_player = False
            self.progress = FLY
            
            directionFacings = [DirectionEnum.UP, DirectionEnum.DOWN,
                               DirectionEnum.LEFT, DirectionEnum.RIGHT]
            directionfacing = self.directionFacing
            while directionfacing == self.directionFacing:
                directionfacing = random.choice(directionFacings)
            self.directionFacing = directionfacing

            if self.directionFacing == DirectionEnum.DOWN:
                self.move_to_force(random.randint(3 * TILE_SCALE, 15 * TILE_SCALE), 
                                   -6 * TILE_SCALE)
            elif self.directionFacing == DirectionEnum.LEFT:
                self.move_to_force(21 * TILE_SCALE,
                                   random.randint(-4 * TILE_SCALE, 6 * TILE_SCALE))
                self.progress *= 1.5
            elif self.directionFacing == DirectionEnum.RIGHT:
                self.move_to_force(-4 * TILE_SCALE,
                                   random.randint(4 * TILE_SCALE, 6 * TILE_SCALE))
                self.progress *= 1.5
            else: 
                self.move_to_force(random.randint(3 * TILE_SCALE, 15 * TILE_SCALE),
                                   12 * TILE_SCALE)

        if self.hit_player: return
        if self.hitbox.colliderect(self.player.hitbox):
            self.player.takeDamage(1)
            self.hit_player = True
    
    def onHit(self, damage: float, attack_id: int) -> None:
        super().onHit(damage, attack_id)

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 0, 0), self.hitbox) 
        super().draw(display)
        health_surface = pygame.Surface((1010, 30))
        health_surface.fill((0, 0, 0))
        health_amount = pygame.Surface(((self.health / HEALTH) * 1000, 20))
        health_amount.fill((255, 0, 0))
        display.blit(
            health_surface, (SIZE[0] // 2 - health_surface.get_width() // 2, 40)
        )
        display.blit(
            health_amount, (SIZE[0] // 2 - health_amount.get_width() // 2, 40)
        )
    
