import pygame


from variables import FPS, SIZE

pygame.init()
delta = 0
display = pygame.display.set_mode((SIZE[0], SIZE[1]))


from objects.object import Object
import objects.knight as knight
import objects.enemy.enemy as enemy
from generation.generation import Generation
from objects.HealthBar import HealthAndCoinBar
from objects.DeathScreen import DeathScreen
from objects.note import Note

def main():
    clock = pygame.time.Clock()
    objects: list[Object] = []

    generation = Generation()
    deathScreen = DeathScreen(display)

    objects.append(generation)

    player = knight.Knight()
    player.move_to_force(400, 400)
    generation.create_map(player)
    
    note = Note(pygame.Vector2(380, 385), player)

    healthBar = HealthAndCoinBar(display)
    healthBar.passPlayerReference(player)

    objects.append(player)
    objects.append(note)
    

    while True:
        delta = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        
        if player.currentHealth > 0:
            display.fill("purple") 

            checks = [obj for obj in objects + generation.map.get_room().objects if not isinstance(obj, enemy.Enemy) or obj.alive]
            
            for object in checks:
                object.update(delta, generation.map, objects)

            for object in checks:
                object.draw(display)
            
            healthBar.draw(delta)

        else:
            deathScreen.draw(delta)
            if deathScreen.isRestarting():
                deathScreen.restarting = False
                return

        pygame.display.flip()

        

if __name__ == "__main__":
    while True:
        main()