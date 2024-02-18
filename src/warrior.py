import pygame
from pygame.locals import *


vec = pygame.math.Vector2
ACC = 0.5
FRIC = -0.12
HEIGHT = 720
WIDTH = 1080


# class représentant nos personnages
class Warrior(pygame.sprite.Sprite):

    def __init__(self, team, pos):
        # initialisation de la superclass sprite
        super().__init__()

        # team du warrior (rouge ou bleu)
        self.team = team

        # position de départ du warrior
        self.pos = pos

        # point de vie du personnage
        self.health = 100
        self.max_health = 100

        # point d'action du personnage
        self.points_action = 100
        self.max_points_action = 100

        # degat du personnage
        self.attack = 10

        self.selected = False

        # image représentant le personnage
        if team == 0:
            self.image = pygame.image.load('../assets/soldat_bleu.png')
            self.image = pygame.transform.scale(self.image, (506/14, 840/14))
        elif team == 1:
            self.image = pygame.image.load('../assets/soldat_rouge.png')
            self.image = pygame.transform.scale(self.image, (506/14, 840/14))
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self, game):
        """gère, par frame, les collisions, déplacement et action"""

        #Applique la gravité au guerrier
        self.acc = vec(0, 0.5)

        self.handle_collisions(game.all_plateformes)
        if game.displacement_phase:
            self.process_input(game)
        self.update_position()
        self.constrain_to_screen()

    def handle_collisions(self, platforms):
        """Gère les collisions avec les plateformes."""
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0 and hits:
            self.vel.y = 0
            self.pos.y = hits[0].rect.top + 1

    def process_input(self, game):
        """Traite les entrées du joueur pour le mouvement et les actions."""
        pressed_keys = pygame.key.get_pressed()
        if self.selected:
            if pressed_keys[K_LEFT]:
                game.have_displace = True
                self.acc.x = -ACC
                self.points_action -= 2
            if pressed_keys[K_RIGHT]:
                game.have_displace = True
                self.acc.x = ACC
                self.points_action -= 2
            if pressed_keys[K_SPACE] and self.vel.y == 0:
                game.have_displace = True
                self.vel.y = -10
                self.points_action -= 20

    def update_position(self):
        """Met à jour la position et la vélocité du guerrier."""
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def constrain_to_screen(self):
        """Empêche le guerrier de sortir des limites de l'écran."""
        if self.pos.x > WIDTH - self.rect.width / 2:
            self.pos.x = WIDTH - self.rect.width / 2
            self.vel.x = 0
        if self.pos.x < self.rect.width / 2:
            self.pos.x = self.rect.width / 2
            self.vel.x = 0
        self.rect.midbottom = self.pos

