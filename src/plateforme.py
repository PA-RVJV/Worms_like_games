import pygame

vec = pygame.math.Vector2
ACC = 0.5
FRIC = -0.12
HEIGHT = 720
WIDTH = 1080


class Plateforme(pygame.sprite.Sprite):
    def __init__(self, largeur_platform, longueur_platform, centre_platform_x, centre_platform_y, platform_color=None):
        super().__init__()
        self.image = pygame.Surface((largeur_platform, longueur_platform))
        if platform_color is None:
            self.image.set_alpha(0)
        else:
            self.image.fill(platform_color)
        self.rect = self.image.get_rect(center=(centre_platform_x, centre_platform_y))

    def update(self, game):
        pass
