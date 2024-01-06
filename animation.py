import pygame

class AnimateSprite(pygame.sprite.Sprite) :
    def __init__(self) :
        super().__init__() # récupère la classe mère permettant l'introduction des sprites
        
        # variables locales à la classe 
        self.sprite_sheet = pygame.image.load("aventurier_1.png") # récupère l'image de l'aventurier
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0), # image 1 regardant vers le bas
            'left': self.get_images(32), # image 2 ... gauche
            'right': self.get_images(64), # ... droite
            'up': self.get_images(96), # ... haut
            }
        self.speed = 0.7 # vitesse de base du joueur
        
    def change_animation(self, name):
        """Récupère l'image correspondant au déplacement actuel"""
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([255, 255, 255])
        self.clock += self.speed * 6
        
        if self.clock >= 100:
            
            self.animation_index += 1
            if self.animation_index >= len(self.images[name]) :
                self.animation_index = 0
            self.clock = 0
            
        
    def get_images(self, y) :
        """Récupère l'image correspondant à l'animation actuelle qui s'actualise"""
        
        images = []
        for i in range(0, 3) :
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)
            
        return images
        
    def get_image(self, x, y):
        """Récupère les paramètres de l'image sélectionnée"""
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image