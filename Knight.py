import pygame

class Knight:

    
    def __init__(self, display):
        self.display = display
        self.spritesheet = pygame.image.load("Assets\Spritesheet_with_Shadows.png").convert_alpha()
        self.knightSprite = self.spritesheet.subsurface(pygame.Rect(0, 0, 48, 48))
        self.knightSprite = pygame.transform.scale(self.knightSprite, (96, 96))
        self.__pos = pygame.Vector2(0, 0)


    def update(self, delta):
        self.display.blit(self.knightSprite, self.__pos)