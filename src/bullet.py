import math

import pygame
from explosion import Explosion
from warrior import Warrior

width_screen = 1080
height_screen = 720

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, speed=40):
        super().__init__()
        self.damage = 10
        self.image = pygame.image.load('../assets/bullet.png')
        self.image = pygame.transform.scale(self.image, (726 / 30, 726 / 30))
        self.image = pygame.transform.rotate(self.image, -math.degrees(angle))  # Oriente le projectile
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = speed
        self.velocity = [math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed]
        pass

    def update(self, game):
        # applique la gravité au projectile
        self.velocity[1] += 0.05

        # Mise à jour de la position du projectile
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.handle_collision(game)
        self.handle_offscreen()

    def handle_collision(self, game):
        hits = pygame.sprite.spritecollide(self, game.all_killable_sprites, False)
        if hits:
            self.kill()
            explosion = Explosion(self.rect.center, radius=5)  # Création de l'effet d'explosion
            game.all_draw_sprites.add(explosion)  # Ajout de l'explosion au groupe de sprites pour l'affichage et la mise à jour
            for sprites in hits:
                if type(sprites) == Warrior:
                    sprites.health -= self.damage
            """# Vérifier si des warriors sont dans la zone d'effet
            for warrior in game.all_warriors:
                if math.hypot(warrior.rect.centerx - self.rect.centerx,
                              warrior.rect.centery - self.rect.centery) < explosion.radius:
                    warrior.health -= self.damage"""

    def handle_offscreen(self):
        # supprime le sprite s'il sort de l'écran
        if self.rect.right < 0 or self.rect.left > width_screen or self.rect.bottom < 0 or self.rect.top > height_screen:
            self.kill()
