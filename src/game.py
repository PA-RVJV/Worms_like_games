import math

import pygame

from bullet import Bullet
from rocket import Rocket
from grenade import Grenade
from plateforme import Plateforme
from warrior import Warrior

# Constantes globales
vec = pygame.math.Vector2

BACKGROUND_IMAGE = "../assets/background_screen.jpg"
WIDTH_SCREEN = 1080
HEIGHT_SCREEN = 720
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255)
WALL_COLOR = (150, 125, 100)


# class représentant le jeu
class Game:
    """Classe de gestion des élément du jeu"""

    def __init__(self):
        """Initialise les éléments du jeu."""
        self.projectile_start_pos = None
        self.players_warriors = [[], []]
        self.current_player = 0
        self.current_warrior_index = 0
        self.all_draw_sprites = pygame.sprite.Group()
        self.all_killable_sprites = pygame.sprite.Group()
        self.all_plateformes = pygame.sprite.Group()
        self.all_projectiles = pygame.sprite.Group()
        self.all_warriors = pygame.sprite.Group()
        self.fire_phase = False
        self.displacement_phase = False
        # 0 pour bullet, 1 pour grenade, 2 pour rocket
        self.projectile_selected = 0

        self.have_attack = False
        self.have_displace = False

        """Initialise l'affichage du jeu."""
        self.screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        pygame.display.set_caption('Jeux "Worms" style')
        self.button_pass_turn = pygame.Rect(WIDTH_SCREEN - 450, HEIGHT_SCREEN - 60, 130, 30)
        self.button_attack = pygame.Rect(WIDTH_SCREEN - 300, HEIGHT_SCREEN - 60, 130, 30)
        self.button_displacement = pygame.Rect(WIDTH_SCREEN - 150, HEIGHT_SCREEN - 60, 130, 30)
        self.button_bullet = pygame.Rect(WIDTH_SCREEN - 450, HEIGHT_SCREEN - 120, 130, 30)
        self.button_grenade = pygame.Rect(WIDTH_SCREEN - 300, HEIGHT_SCREEN - 120, 130, 30)
        self.button_rocket = pygame.Rect(WIDTH_SCREEN - 150, HEIGHT_SCREEN - 120, 130, 30)
        self.background = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE).convert(),
                                                 (WIDTH_SCREEN, HEIGHT_SCREEN))

    def add_warrior(self, warrior: Warrior):
        """Ajoute un guerrier au jeu."""
        self.players_warriors[warrior.team].append(warrior)
        self.all_draw_sprites.add(warrior)
        self.all_killable_sprites.add(warrior)
        self.all_warriors.add(warrior)
        if warrior.team == 0 and len(self.players_warriors[0]) == 1:
            warrior.selected = True  # Sélectionne le premier guerrier du joueur 1 par défaut

    def add_platform(self, platform: Plateforme):
        """Ajoute une plateforme au jeu."""
        self.all_draw_sprites.add(platform)
        self.all_plateformes.add(platform)
        self.all_killable_sprites.add(platform)

    def add_projectile(self, projectile):
        """Ajoute un projectile au jeu."""
        self.all_draw_sprites.add(projectile)
        self.all_projectiles.add(projectile)

    def init_game(self):
        """Rétablie tout les paramètre a leurs état d'origine et instancie les sprites de jeu"""
        self.projectile_start_pos = None
        self.players_warriors = [[], []]
        self.current_player = 0
        self.current_warrior_index = 0
        self.all_draw_sprites = pygame.sprite.Group()
        self.all_plateformes = pygame.sprite.Group()
        self.all_projectiles = pygame.sprite.Group()
        self.all_warriors = pygame.sprite.Group()
        self.fire_phase = False
        self.displacement_phase = False
        self.have_attack = False
        self.have_displace = False

        plateformes = [
            # plateforme sol principale
            Plateforme(largeur_platform=WIDTH_SCREEN, longueur_platform=20, centre_platform_x=WIDTH_SCREEN / 2, centre_platform_y=530),
            # plateforme mur
            #Plateforme(largeur_platform=20, longueur_platform=HEIGHT_SCREEN/5, centre_platform_x=WIDTH_SCREEN / 2, centre_platform_y=340, platform_color=WALL_COLOR),
            # plateforme de start player 1
            Plateforme(largeur_platform=160, longueur_platform=20, centre_platform_x=160 / 2, centre_platform_y=370),
            # plateforme de start player 2
            Plateforme(largeur_platform=135, longueur_platform=20, centre_platform_x=WIDTH_SCREEN - (135 / 2), centre_platform_y=370)
        ]

        warriors = [Warrior(0, vec((70, 385))), Warrior(1, vec((1000, 385)))]

        for warrior in warriors:
            self.add_warrior(warrior)

        for plateforme in plateformes:
            self.add_platform(plateforme)

    def handle_mouse_button_down(self, event):
        """Gère les clics de souris."""

        # clic sur bouton attaque
        if self.button_attack.collidepoint(event.pos) and not self.fire_phase and not self.have_attack:
            self.fire_phase = True
            self.displacement_phase = False
        elif self.button_attack.collidepoint(event.pos) and self.fire_phase:
            self.fire_phase = False
        elif self.fire_phase and not self.have_attack:
            self.fire_projectile()
            self.have_attack = True
            self.fire_phase = False

        # clic sur bouton deplacement
        elif self.button_displacement.collidepoint(event.pos) and not self.displacement_phase and not self.have_displace:
            self.displacement_phase = True
            self.fire_phase = False
        elif self.button_displacement.collidepoint(event.pos) and self.displacement_phase:
            self.displacement_phase = False

        # clic sur bouton bullet
        elif self.button_bullet.collidepoint(event.pos):
            self.projectile_selected = 0

        # clic sur bouton grenade
        elif self.button_grenade.collidepoint(event.pos):
            self.projectile_selected = 1

        # clic sur bouton rocket
        elif self.button_rocket.collidepoint(event.pos):
            self.projectile_selected = 2

        # si le warrior actuelle a deja attaqué et ne ses pas déplacé
        elif self.button_attack.collidepoint(event.pos) and self.have_attack and not self.have_displace:
            self.show_message("Attaque deja effectuer, veuillez vous déplacer ou passer le tour", 1000)

        # si le warrior actuelle n'a pas encore attaqué et ses déplacé
        elif self.button_displacement.collidepoint(event.pos) and not self.have_attack and self.have_displace:
            self.show_message("Mouvement déja effectuer ,veuillez attaquer ou passer le tour", 1000)

        elif self.button_pass_turn.collidepoint(event.pos):
            self.change_player()

        elif not self.fire_phase and not self.displacement_phase and self.have_attack and self.have_displace:
            self.show_message("Le soldat n'a plus d'action disponible, veuillez passer le tour", 1000)

    def change_player(self):
        """change le warrior actif/passe le tour"""
        # Récupère la liste des guerriers du joueur actuel
        current_warriors = self.players_warriors[self.current_player]

        # Désélectionne le guerrier actuel et vérifie s'il doit passer au guerrier suivant ou au joueur suivant
        current_warrior = current_warriors[self.current_warrior_index]
        self.have_displace = False
        self.have_attack = False
        current_warrior.selected = False
        current_warrior.points_action = current_warrior.max_points_action  # Réinitialise les points d'action pour le prochain tour

        # Passe au guerrier suivant ou au joueur suivant
        self.current_warrior_index += 1
        if self.current_warrior_index >= len(current_warriors):
            # Tous les guerriers du joueur actuel ont joué, passe au joueur suivant
            self.current_warrior_index = 0
            self.current_player = (self.current_player + 1) % len(self.players_warriors)
            self.show_message(f"Player {self.current_player + 1} play!")
            # Sélectionne le premier guerrier du joueur suivant
            if self.players_warriors[self.current_player]:  # Vérifie si le joueur suivant a des guerriers
                self.players_warriors[self.current_player][0].selected = True
        else:
            # Passe au guerrier suivant du même joueur
            current_warriors[self.current_warrior_index].selected = True
            self.show_message(
                f"Player {self.current_player + 1}, warrior {self.current_warrior_index + 1}'s turn")

    def draw_sight_target(self, screen, warrior: Warrior):
        """Dessine la ligne de visée."""
        # variable d'ajustement de la position centrale du warrior (pour l'image choisie)
        offset_x = 0
        offset_y = 32

        # Position de départ ajustée de la ligne de visée
        sight_start_pos = (warrior.pos[0] + offset_x, warrior.pos[1] - offset_y)

        mouse_pos = pygame.mouse.get_pos()
        self.angle_visee = self.calculate_angle_sight(sight_start_pos, mouse_pos)
        # Dessine un trait entre le guerrier et la position du curseur de la souris
        pygame.draw.line(screen, WHITE_COLOR, sight_start_pos, mouse_pos, 2)  # 2 est l'épaisseur du trait

    def fire_projectile(self):
        """Gère le tir d'un projectile."""
        for warrior in self.players_warriors[self.current_player]:
            if warrior.selected:
                # Calcul de l'angle de visée en fonction de la position (ajustée à l'image) du warrior et de la souris
                angle_visee = self.calculate_angle_sight((warrior.pos[0], warrior.pos[1] - 32), pygame.mouse.get_pos())

                # Rayon du cercle imaginaire autour du warrior
                radius = 100  # Ajustez selon la taille du sprite du warrior et l'effet désiré

                # Calcul du point de départ du projectile sur le cercle basé sur l'angle de visée
                offset_x = math.cos(angle_visee) * radius
                offset_y = math.sin(angle_visee) * radius

                projectile_start_pos = (warrior.pos[0] + offset_x, warrior.pos[1] + offset_y - 32)

                # Ajoute le projectile avec le type sélectionné
                if self.projectile_selected == 0:
                    self.add_projectile(Bullet(projectile_start_pos, angle_visee))
                elif self.projectile_selected == 1:
                    self.add_projectile(Grenade(projectile_start_pos, angle_visee))
                elif self.projectile_selected == 2:
                    self.add_projectile(Rocket(projectile_start_pos, angle_visee))

    def update(self):
        """Update le jeu a chaque frame (dessin et etat)"""
        # Récupère la liste des guerriers du joueur actuel
        current_warriors = self.players_warriors[self.current_player]
        # Désélectionne le guerrier actuel et vérifie s'il doit passer au guerrier suivant ou au joueur suivant
        current_warrior = current_warriors[self.current_warrior_index]
        if current_warrior.points_action < 2:
            self.displacement_phase = False
        self.draw()
        self.verify_health()
        self.verify_victory()

    def verify_victory(self):
        """Verifie les conditions de victoire pour restart le game en cas de victoire de l'une des equipe"""
        team_counts = [len(team) for team in self.players_warriors]

        # Vérifier si l'une des équipes n'a plus de warriors
        if team_counts[0] == 0 or team_counts[1] == 0:
            winning_team = 1 if team_counts[0] == 0 else 0
            self.show_message(f"L'équipe {winning_team + 1} gagne la partie !", 5000)
            self.init_game()

    def verify_health(self):
        """Vérifie la santé des warrior pour detruire ceux qui n'en ont plus"""
        for team in self.players_warriors:
            for warrior in team[:]:
                if warrior.health <=0:
                    warrior.kill()
                    team.remove(warrior)

    def draw(self):
        """Dessine les éléments du jeu à l'écran."""
        self.screen.blit(self.background, (0, 0))
        for entity in self.all_draw_sprites:
            self.screen.blit(entity.image, entity.rect)
            entity.update(self)
            if isinstance(entity, Warrior):
                health_bar_x = entity.rect.x + (entity.rect.width / 2) - 20
                health_bar_y = entity.rect.y - 10
                self.draw_health_bar(self.screen, health_bar_x, health_bar_y, entity.health, max_health=entity.max_health, bar_length=40, bar_height=5)

        for warrior in self.players_warriors[self.current_player]:
            if warrior.selected:
                self.draw_interface(warrior)

    def draw_interface(self, warrior):
        """Dessine l'interface utilisateur pour le guerrier actif."""
        self.draw_button(self.screen, self.button_pass_turn, "Pass", BLUE_COLOR)
        if self.fire_phase:
            self.draw_sight_target(self.screen, warrior)
            self.draw_button(self.screen, self.button_attack, "Attack", BLUE_COLOR)
            pygame.draw.rect(self.screen, RED_COLOR, self.button_attack, 3)
        else:
            self.draw_button(self.screen, self.button_attack, "Attack", BLUE_COLOR)

        if self.displacement_phase:
            self.draw_button(self.screen, self.button_displacement, "Move", BLUE_COLOR)
            pygame.draw.rect(self.screen, RED_COLOR, self.button_displacement, 3)
        else:
            self.draw_button(self.screen, self.button_displacement, "Move", BLUE_COLOR)

        if self.projectile_selected == 0:
            self.draw_button(self.screen, self.button_bullet, "Bullet", GREEN_COLOR)
            pygame.draw.rect(self.screen, RED_COLOR, self.button_bullet, 3)
        else:
            self.draw_button(self.screen, self.button_bullet, "Bullet", GREEN_COLOR)

        if self.projectile_selected == 1:
            self.draw_button(self.screen, self.button_grenade, "Grenade", GREEN_COLOR)
            pygame.draw.rect(self.screen, RED_COLOR, self.button_grenade, 3)
        else:
            self.draw_button(self.screen, self.button_grenade, "Grenade", GREEN_COLOR)

        if self.projectile_selected == 2:
            self.draw_button(self.screen, self.button_rocket, "Rocket", GREEN_COLOR)
            pygame.draw.rect(self.screen, RED_COLOR, self.button_rocket, 3)
        else:
            self.draw_button(self.screen, self.button_rocket, "Rocket", GREEN_COLOR)

        self.draw_PA_bar(self.screen, 50 + 250, HEIGHT_SCREEN - 50, warrior.points_action, warrior.max_points_action)



    def draw_health_bar(self, screen, x, y, health, max_health, bar_length=40, bar_height=5):
        """Dessine la barre de vie au dessus du warrior"""
        if health < 0:
            health = 0
        fill = (health / max_health) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(screen, RED_COLOR, outline_rect)
        pygame.draw.rect(screen, GREEN_COLOR, fill_rect)
        pygame.draw.rect(screen, BLACK_COLOR, outline_rect, 1)

    def draw_PA_bar(self, screen, x, y, point_action, max_point_action):
        """Dessine la barre de points d'action."""
        if point_action < 0:
            point_action = 0
        bar_length = 200
        bar_height = 20
        fill = (point_action / max_point_action) * bar_length
        outline_rect = pygame.Rect(x, y, bar_length, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(screen, RED_COLOR, outline_rect)
        pygame.draw.rect(screen, BLUE_COLOR, fill_rect)
        pygame.draw.rect(screen, BLACK_COLOR, outline_rect, 2)

    def draw_button(self, screen, button, text, color):
        """Dessine le bouton de tir."""
        pygame.draw.rect(screen, color, button)
        font_button = pygame.font.Font(None, 24)
        text = font_button.render(text, True, WHITE_COLOR)
        screen.blit(text, (button.x + 5, button.y + 5))

    def show_message(self, message, duration=3000):
        """Affiche un message à l'écran."""
        font = pygame.font.Font(None, 36)  # Choisissez la taille de police appropriée
        text = font.render(message, True, BLACK_COLOR)  # Blanc
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))
        self.screen.blit(text, text_rect)
        pygame.display.flip()  # Met à jour l'écran pour montrer le message
        pygame.time.delay(duration)  # Attend `duration` millisecondes

    def calculate_angle_sight(self, warrior_pos, mouse_pos):
        """Calcule l'angle de visée."""
        dx = mouse_pos[0] - warrior_pos[0]
        dy = mouse_pos[1] - warrior_pos[1]
        return math.atan2(dy, dx)
