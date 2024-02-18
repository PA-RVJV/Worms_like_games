import pygame
from warrior import Warrior
from plateforme import Plateforme
from game import Game

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# instantie la classe de gestion du jeu
game = Game()
# initialise le jeu
game.init_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_mouse_button_down(event)

    # met a jour le jeux avec tout les éléments
    game.update()

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()