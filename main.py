import pygame

pygame.init()
delta = 0
display = pygame.display.set_mode((1280,720))


from objects.object import Object
import objects.knight as knight
import objects.enemy as enemy
from generation.generation import Generation
from objects.HealthBar import HealthBar
from objects.DeathScreen import DeathScreen

def main():
    clock = pygame.time.Clock()
    objects: list[Object] = []

    generation = Generation()
    deathScreen = DeathScreen(display)
    player : knight.Knight

    objects.append(generation)

    player = knight.Knight(display)
    player.move_to(400, 400, generation.map)

    healthBar = HealthBar(display)
    healthBar.passPlayerReference(player)

    slime1 = enemy.Slime()
    slime1.move_to(400, 400, generation.map)
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
        
        if player.currentHealth > 0:
            
            display.fill("purple") 

            objects = [obj for obj in objects if not isinstance(obj, enemy.Enemy) or obj.alive]
            
            for object in objects:
                object.update(delta, generation.map, objects)

            for object in objects:
                object.draw(display)
            
            healthBar.draw()
        
        else:
            deathScreen.draw(delta)
            if deathScreen.isRestarting():
                deathScreen.restarting = False
                return

        pygame.display.flip()

if __name__ == "__main__":
    while True:
        main()