import math

import pygame
from explosion import Explosion

width_screen = 1080
height_screen = 720

class Grenade(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=5):
        super().__init__()
        self.damage = 100
        self.original_image = pygame.image.load('../assets/grenade.png')
        self.original_image = pygame.transform.scale(self.original_image, (30, 30))
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle))  # Oriente le projectile
        self.rect = self.image.get_rect(center=pos)

        self.angle = angle
        self.speed = speed
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]

        self.creation_time = pygame.time.get_ticks()
        self.fuse_time = 5000  # Durée en millisecondes avant que la grenade explose

    def update(self, game):
        # applique la gravité au projectile
        self.velocity[1] += 0.1

        # Mise à jour de la position du projectile
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Appliquer une rotation constante à la grenade
        self.angle += 5  # Augmente l'angle de 5 degrés à chaque mise à jour pour une rotation constante
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # Applique la rotation
        self.rect = self.image.get_rect(center=self.rect.center)  # Ajuste le rect pour la nouvelle image

        self.handle_collision(game)
        self.detect_offscreen()
        self.explode(game)

    def handle_collision(self, game):
        hits = pygame.sprite.spritecollide(self, game.all_killable_sprites, False)
        if hits:
            # Inverse la direction verticale pour simuler un rebond
            self.velocity[1] = -self.velocity[1] * 0.7  # Applique un facteur de rebond pour réduire la vitesse
            self.velocity[0] = self.velocity[0] * 0.9  # Applique un facteur de frottement pour réduire la vitesse horizontale

            # Ajuste la position pour éviter de rester bloqué dans l'objet avec lequel la grenade a collisionné
            self.rect.y += self.velocity[1]
            self.rect.x += self.velocity[0]

    def detect_offscreen(self):
        # Supprime le sprite s'il sort des limite horizontale de l'écran ou si elle sort par le bas
        if self.rect.right < 0 or self.rect.left > width_screen or self.rect.top > height_screen:
            self.kill()

    def explode(self, game):
        # Vérifier si le temps de la mèche est écoulé pour déclencher l'explosion
        if pygame.time.get_ticks() - self.creation_time > self.fuse_time:
            # Supprimez le sprite grenade
            self.kill()
            # Créez ici l'effet d'explosion et gérez les dégâts aux warriors
            explosion = Explosion(self.rect.center, radius=80)  # Utilisez la classe Explosion définie précédemment
            game.all_draw_sprites.add(explosion)

            for warrior in game.all_warriors:
                if math.hypot(warrior.rect.centerx - self.rect.centerx,
                              warrior.rect.centery - self.rect.centery) < explosion.radius:
                    warrior.kill()  # Suppression des warriors touchés par l'explosion


