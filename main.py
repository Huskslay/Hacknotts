import pygame
from objects.object import Object

pygame.init()
delta = 0
display = pygame.display.set_mode((1280,720))


import objects.knight as knight
import objects.enemy as enemy

clock = pygame.time.Clock()

objects: list[Object] = []

player = knight.Knight(display)
slime1 = enemy.Slime(display)
objects.append(player)
objects.append(slime1)

for object in objects:
    if isinstance(object, enemy.Enemy):
        object.passPlayerReference(player)

while True:
    delta = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    display.fill("purple") 
    
    for object in objects:
        object.update(delta)

    for object in objects:
        object.draw(display)

    pygame.display.flip()