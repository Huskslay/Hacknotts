import pygame, math

DEATHTEXTSIZE = 8
DEATHSKULLSIZE = 60
RESTARTSIZE = 3
SKULLROTATIONSIZE = 30
SKULLROTATIONSLOW = 800
TEXTOSCILLATIONSLOW = 300
TEXTOSCILLATIONSIZE = 50
RESTARTOSCILLATIONSLOW = 500
RESTARTOSCILLATIONSIZE = 20
RESTART_TEXT_X = 1000
RESTART_TEXT_Y = 600

class DeathScreen():
    def __init__(self, display) -> None:
        self.display = display
        self.textSprite = pygame.image.load("Assets\\DeathScreenAssets\\DeathText.png").convert_alpha()
        self.skullSprite = pygame.image.load("Assets\\DeathScreenAssets\\DeathSkull.png").convert_alpha()
        self.restartTextSprite = pygame.image.load("Assets\\DeathScreenAssets\\RestartText.png").convert_alpha()
        self.restartGlowSprite = pygame.image.load("Assets\\DeathScreenAssets\\RestartGlow.png").convert_alpha()
        self.textSprite = pygame.transform.scale(self.textSprite, (58 * DEATHTEXTSIZE, 32 * DEATHTEXTSIZE)) 
        self.skullSprite = pygame.transform.scale(self.skullSprite, (11 * DEATHSKULLSIZE, 10 * DEATHSKULLSIZE)) 
        self.restartTextSprite = pygame.transform.scale(self.restartTextSprite, (72 * RESTARTSIZE, 21 * RESTARTSIZE)) 
        self.restartGlowSprite = pygame.transform.scale(self.restartGlowSprite, (83 * RESTARTSIZE, 29 * RESTARTSIZE)) 
        self.restart_rect = self.restartTextSprite.get_rect(topleft=(RESTART_TEXT_X, RESTART_TEXT_Y))
        self.deltatotal = 0
        self.isHovering = False
        self.restarting = False


    def draw(self, delta) -> None:
        self.deltatotal += delta
        self.display.fill((40, 40, 40)) 
        self.renderInDeathText()
        self.renderInDeathSkull()
        self.checkForInputs()
        self.renderInRestart()


    def passPlayerReference(self, player) -> None:
        self.player = player
    
    def renderInDeathSkull(self):
        skullPos = self.skullSprite.get_rect(center=self.display.get_rect().center)
        skull_x, skull_y = skullPos.topleft
        self.display.blit(self.skullSprite, (
            int(skull_x + math.sin(self.deltatotal / SKULLROTATIONSLOW) * SKULLROTATIONSIZE), 
            int(skull_y + math.cos(self.deltatotal/ SKULLROTATIONSLOW) * SKULLROTATIONSIZE)
        ))
    
    def renderInDeathText(self):
        textPos = self.textSprite.get_rect(center=self.display.get_rect().center)
        text_x, text_y = textPos.topleft
        self.display.blit(self.textSprite, (
            text_x, 
            int(text_y + math.cos(self.deltatotal/ TEXTOSCILLATIONSLOW) * TEXTOSCILLATIONSIZE)
        ))
    
    def renderInRestart(self):
        text_x, text_y = RESTART_TEXT_X, RESTART_TEXT_Y
        self.display.blit(self.restartTextSprite, (
            text_x, 
            int(text_y + math.cos(self.deltatotal/ RESTARTOSCILLATIONSLOW) * RESTARTOSCILLATIONSIZE)
        ))

        if self.isHovering:
            text_x, text_y = RESTART_TEXT_X - 5 * RESTARTSIZE, RESTART_TEXT_Y - 5 * RESTARTSIZE
            self.display.blit(self.restartGlowSprite, (
                text_x, 
                int(text_y + math.cos(self.deltatotal/ RESTARTOSCILLATIONSLOW) * RESTARTOSCILLATIONSIZE)
            ))

    def checkForInputs(self):
        mousePos = pygame.mouse.get_pos()
        yOffset = int(math.cos(self.deltatotal / RESTARTOSCILLATIONSLOW) * RESTARTOSCILLATIONSIZE)
        current_rect = self.restart_rect.move(0, yOffset)

        if current_rect.collidepoint(mousePos):
            self.isHovering = True
        else:
            self.isHovering = False

        mouseClicks = pygame.mouse.get_pressed()
        if self.isHovering and mouseClicks[0]:
            self.restarting = True
    
    def isRestarting(self) -> bool :
        return self.restarting