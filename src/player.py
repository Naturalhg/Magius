import pygame
from animation import AnimateSprite # récupère la classe AnimateSprite()

class Player(AnimateSprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.animation = AnimateSprite()
        self.image = self.get_image(self.animation.PERSO[4]+32, self.animation.PERSO[0])
        self.image.set_colorkey(self.animation.BACK_COLOR)
        self.rect = self.image.get_rect() # récupère la position du joueur
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12) # récupère le rectangle représentant la position du joueur par ses pieds
        self.old_position = self.position.copy() # copie l'ancienne position du joueur

    def save_location(self) :
        """Fait une copie de l'ancienne position du joueur"""
        self.old_position = self.position.copy()

    def move_right(self):
        """Déplacement vers la droite"""
        self.position[0] += self.speed # ajoute la vitesse (en pixels) à la position du joueur à chaque actualisation(120 fps ici)
        
    def move_left(self):
        """Déplacement vers la gauche"""
        self.position[0] -= self.speed
        
    def move_up(self):
        """Déplacement vers le haut"""
        self.position[1] -= self.speed
        
    def move_down(self):
        """Déplacement vers le bas"""
        self.position[1] += self.speed
        
    def speed_move_right(self):
        """Déplacement rapide vers la droite"""
        self.position[0] += self.speed * 1.6 # multiplie la vitesse actuelle par 1,6 pour augmenter la vitesse du joueur
        
    def speed_move_left(self):
        """Déplacement rapide vers la gauche"""
        self.position[0] -= self.speed * 1.6
        
    def speed_move_up(self):
        """Déplacement rapide vers le haut"""
        self.position[1] -= self.speed * 1.6
        
    def speed_move_down(self):
        """Déplacement rapide vers le bas"""
        self.position[1] += self.speed * 1.6
        
    def update(self) :
        """Actualise la position du joueur"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
    def move_back(self) :
        """Permet de rectifier les problèmes d'animation dus aux collisions"""
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
      