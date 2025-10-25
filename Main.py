import pygame

pygame.init()
delta = 0
display = pygame.display.set_mode((1280,720))

import Knight

clock = pygame.time.Clock()

knight = Knight.Knight(display)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    display.fill("purple") 
    knight.update(delta)

    pygame.display.flip()  # Refresh on-screen display
    delta = clock.tick(60)         # wait until next frame (at 60 FPS)