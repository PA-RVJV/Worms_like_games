import math

import pygame
from explosion import Explosion

width_screen = 1080
height_screen = 720

class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=10):
        super().__init__()
        self.damage = 100
        self.original_image = pygame.image.load('../assets/missile.png')
        self.original_image = pygame.transform.scale(self.original_image, (726 / 20, 726 / 20))
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle))  # Oriente le projectile
        self.rect = self.image.get_rect(center=pos)

        self.angle = angle
        self.speed = speed
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]

    def update(self, game):
        # applique la gravité au projectile
        self.velocity[1] += 0.1

        # Mise à jour de la position du projectile
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Calculer le nouvel angle de l'image basé sur la direction de déplacement
        direction_angle = math.atan2(self.velocity[1], self.velocity[0])
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(direction_angle))
        self.rect = self.image.get_rect(center=self.rect.center)  # Mise à jour du rect pour conserver la position

        self.handle_collision(game)
        self.handle_offscreen()

    def handle_collision(self, game):
        hits = pygame.sprite.spritecollide(self, game.all_killable_sprites, False)
        if hits:
            self.kill()
            explosion = Explosion(self.rect.center, radius=50)  # Création de l'effet d'explosion
            game.all_draw_sprites.add(explosion)  # Ajout de l'explosion au groupe de sprites pour l'affichage et la mise à jour

            # Vérifier si des warriors sont dans la zone d'effet
            for warrior in game.all_warriors:
                if math.hypot(warrior.rect.centerx - self.rect.centerx,
                              warrior.rect.centery - self.rect.centery) < explosion.radius:
                    warrior.health -= self.damage  # Suppression des warriors touchés par l'explosion

    def handle_offscreen(self):
        # Supprime le sprite s'il sort des limite horizontale de l'écran ou si elle sort par le bas
        if self.rect.right < 0 or self.rect.left > width_screen or self.rect.top > height_screen:
            self.kill()
