import pygame

BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255)


class Explosion(pygame.sprite.Sprite):
    """Classe pour l'affichage des explosion pour les projectiles rocket et grenade"""
    def __init__(self, center, radius=50):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.animation_time = 1000  # Durée de l'animation en millisecondes
        self.creation_time = pygame.time.get_ticks()

    def update(self, game):
        # Animation clignotante rouge et jaune
        elapsed_time = pygame.time.get_ticks() - self.creation_time
        if elapsed_time > self.animation_time:
            self.kill()  # Fin de l'animation, suppression de l'explosion
        else:
            if elapsed_time % 100 < 50:  # Clignotement toutes les 100 ms
                color = (255, 0, 0)  # Rouge
            else:
                color = (255, 255, 0)  # Jaune
            pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)