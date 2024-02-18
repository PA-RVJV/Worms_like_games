import pygame
from game import Game
from warrior import Warrior
from platform import Platform

pygame.init()

# dimension de la fenêtre de jeu
width_screen = 1080
height_screen = 720

# generation de la fenêtre de jeu
screen = pygame.display.set_mode((width_screen, height_screen))
pygame.display.set_caption('Jeux "Worms" style')

# charge une platform
PT1 = Platform()
player1 = Warrior()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(player1)

running = True
while running:

    # applique l'image de fond à l'arrière plan du jeu
    screen.blit(background, (0, 0))

    # appliquer l'image du warrior1
    screen.blit(game.warrior.image, game.warrior.rect)

    # recupere les projectiles actuel
    for projectile in game.warrior.all_projectiles:
        projectile.move_missile()


    # appliquer l'ensemble des image du groupe de projectiles
    game.warrior.all_projectiles.draw(screen)

    # verifie les touche presser
    if game.pressed.get(pygame.K_RIGHT) and game.warrior.rect.x + game.warrior.rect.width < screen.get_width():
        game.warrior.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.warrior.rect.x > 0:
        game.warrior.move_left()

    # met à jour l'écran
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        # si un joueur appuis sur une touche du clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_RIGHT:
                game.warrior.rotate()

            if event.key == pygame.K_LEFT:
                game.warrior.rotate()

            # detecte si la touche espace est enclenché
            if event.key == pygame.K_SPACE:
                game.warrior.launch_missile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

