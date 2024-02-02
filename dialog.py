import pygame

class Dialog_box() :
    
    #variables pricipales des coordonnées en X et en Y de la bulle
    X_POSITION = 60
    Y_POSITION = 470
    
    def __init__(self) :
        self.box = pygame.image.load('dialog_box.png') #récupère la bulle de discussion
        self.box = pygame.transform.scale(self.box, (1200, 210))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('dialogs1.ttf', 48) #récupère la police d'écriture
        self.lecture = False
        self.end_text = False
        
    def execute(self, dialog) :
        """Met en lien les deux methodes ci-dessous pour afficher et faire défiler correctement le dialogue demandé"""
        if self.lecture :
            self.next_text()
        else :
            self.lecture = True
            self.text_index = 0
            self.texts = dialog
        
    def render(self, screen) :
        """Affiche la bulle de dialogue et son texte"""
        if self.lecture :
            self.end_text = False
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]) :
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            txt = self.font.render(self.texts[self.text_index], False, (0, 0, 0))
            screen.blit(txt, (self.X_POSITION + 100, self.Y_POSITION + 70)) 
    
    def render_slow(self, screen) :
        """Affiche la bulle de dialogue et ses lettres une par une"""
        if self.lecture :
            self.letter_index += 1
            if self.letter_index >= len(self.texts[self.text_index]) :
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            txt = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(txt, (self.X_POSITION + 100, self.Y_POSITION + 70))
        
    def next_text(self) :
        """Indente les variables et ferme la bulle"""
        self.text_index += 1
        self.letter_index = 0
        
        if self.text_index >= len(self.texts) :
            #ferme la bulle
            self.end_text = True
            self.lecture = False