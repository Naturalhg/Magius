import pygame

class AnimateSprite(pygame.sprite.Sprite) :
    """ Sprites des différents personnages en fonction de leurs pixels
        Pour changer de personnage, copier les coordonnées du personnage
        choisi dans la variable PERSO """
    
    PERSO = [0, 32, 64, 96, 0] # sprite du personnage actuel
    
    #sprites des différents personnages
    """
    PERSO_1 = [0, 32, 64, 96, 0]
    PERSO_2 = [0, 32, 64, 96, 96]
    PERSO_3 = [0, 32, 64, 96, 192]
    PERSO_4 = [0, 32, 64, 96, 288]
    PERSO_5 = [128, 160, 192, 224, 0]
    PERSO_6 = [128, 160, 192, 224, 96]
    PERSO_7 = [128, 160, 192, 224, 192]
    PERSO_8 = [128, 160, 192, 224, 288]
    """

    # Couleur nécessaire qui permet d'avoir un fond transparent pour le personnage
    BACK_COLOR = [255, 255, 255] # fond actuel
    """
    BACK_COLOR_1 = [255, 255, 255] # pour fond blanc
    BACK_COLOR_2 = [0, 0, 0] # pour fond noir
    """

    def __init__(self) :
        super().__init__() # récupère la classe mère permettant l'introduction des sprites

        # variables locales à la classe
        self.sprite_sheet = pygame.image.load("../sprites/aventurier_1.png") # récupère l'image de l'aventurier
        self.animation_index = 0
        self.clock = 0
        self.images = {
                        'down': self.get_images(self.PERSO[0]), # image 1 regardant vers le bas
                        'left': self.get_images(self.PERSO[1]), # image 2 vers la gauche
                        'right': self.get_images(self.PERSO[2]), # image 3 vers la droite
                        'up': self.get_images(self.PERSO[3]), # image 4 vers le haut
                        }
        self.speed = 0.7 # vitesse de base du joueur

    def change_animation(self, name):
        """Récupère l'image correspondant au déplacement actuel"""
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(self.BACK_COLOR)
        self.clock += self.speed * 6

        if self.clock >= 100 :

            self.animation_index += 1
            if self.animation_index >= len(self.images[name]) :
                self.animation_index = 0
            self.clock = 0

    def get_images(self, y) :
        """Récupère l'image correspondant à l'animation actuelle qui s'actualise"""

        images = []
        # récupère les sprites du personnage en fonction des pixels horizontalement
        for i in range(int(self.PERSO[4]/32), int((self.PERSO[4]/32)+3)) :
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self, x, y):
        """Récupère les paramètres de l'image sélectionnée"""
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image