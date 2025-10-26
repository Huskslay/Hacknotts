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
from objects.Shopkeeper import Shopkeeper

def main():
    clock = pygame.time.Clock()
    objects: list[Object] = []

    generation = Generation()
    deathScreen = DeathScreen(display)

    objects.append(generation)

    player = knight.Knight()
    player.move_to_force(400, 400)
    generation.create_map(player)

    healthBar = HealthBar(display)
    healthBar.passPlayerReference(player)


    objects.append(player)

    shopkeeper = Shopkeeper(pygame.Vector2(500, 300))
    shopkeeper.passPlayerReference(player)
    objects.append(shopkeeper)

    while True:
        delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        
        if player.currentHealth > 0:
            
            display.fill("purple") 

            checks = [obj for obj in objects + generation.map.get_room().enemies if not isinstance(obj, enemy.Enemy) or obj.alive]
            
            for object in checks:
                object.update(delta, generation.map, objects)

            for object in checks:
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