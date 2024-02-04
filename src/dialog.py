import pygame

class Dialog_box() :
    
    #variables pricipales des coordonnées en X et en Y de la bulle
    X_POSITION = 60
    Y_POSITION = 470
    
    def __init__(self) :
        self.dialogs = [["^ : Maison", "> : Village", "v : Forêt"], #panneau 1
                        ["^ : Cabane", "< : Maison", "> : Village"], #panneau 2
                        ["^ : Cimetière", "< : Maison", "> : Fontaine", "v : Village"], #panneau 3
                        ["Cette porte est fermée,", "quelqu'un habite ici."], #portes village
                        ["Il n'y a rien dans la boîte aux lettres."], #boîte aux lettres
                        ["Bienvenue dans notre monde,", "découvre ce monde par toi même en t'aidant", "des panneaux et accomplis la quête principale.", "Plus d'informations dans le tableau au village."], #panneau d'introduction
                        ["Quête principale :", "Récupérez les 11 clés réparties sur la carte."],
                        ["Bien joué ! Vous avez trouvé toutes les clés"],
                        ["Vous avez trouvé toutes les clés !", "Que peuvent-elles bien ouvrir..."]
                        ]
        self.box = pygame.image.load('dialogs/boxes/dialog_box.png') #récupère la bulle de discussion
        self.box = pygame.transform.scale(self.box, (1200, 210))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('dialogs/polices/dialogs1.ttf', 48) #récupère la police d'écriture
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