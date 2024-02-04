import pygame

from player import Player
from dialog import Dialog_box
from map_manager import Map_Manager

pygame.init()

class Game() :
    
    ADVENTURE_MODE = 0
    DIALOG_MODE = 1
    
    def __init__(self) :
        self.dialog_box = Dialog_box()
        self.clock = pygame.time.Clock()
        self.running = True
        self.map = 'map'
        self.status = 0
        
        #crée la fenêtre du jeu
        self.screen = pygame.display.set_mode((1350, 700)) #taille
        pygame.display.set_caption("Magius")  #titre
        
        self.player = Player(0,0)
        self.map_manager = Map_Manager(self.screen, self.player)
    
    
    
    def handle_input(self) :
        """Indique le bouton pressé par l'utilisateur et déplace le joueur en conséquence"""
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_z] and pressed[pygame.K_SPACE] or pressed[pygame.K_UP] and pressed[pygame.K_SPACE]: # si 'z' et 'x' sont appuyés :
            self.player.speed_move_up()                  # méthode 'speed_move_up()' de la classe player
            self.player.change_animation('up')           # changement de l'animation 'up'
        elif pressed[pygame.K_s] and pressed[pygame.K_SPACE] or pressed[pygame.K_DOWN] and pressed[pygame.K_SPACE]:
            self.player.speed_move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_q] and pressed[pygame.K_SPACE] or pressed[pygame.K_LEFT] and pressed[pygame.K_SPACE]:
            self.player.speed_move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_d] and pressed[pygame.K_SPACE] or pressed[pygame.K_RIGHT] and pressed[pygame.K_SPACE]:
            self.player.speed_move_right()
            self.player.change_animation('right')
        
        elif pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
    
    def update(self) :
        """Actualise les sprites en fonction des collisions"""
        self.map_manager.update()
    
    def check(self) :
        """Détecte les objets en contact avec le joueur et affiche le texte adapté"""
        if self.player.feet.colliderect(self.map_manager.panneau_1_rect) :
            self.status = self.DIALOG_MODE
            self.dialog_box.execute(self.dialog_box.dialogs[0])
        elif self.player.feet.colliderect(self.map_manager.panneau_2_rect) :
            self.status = self.DIALOG_MODE
            self.dialog_box.execute(self.dialog_box.dialogs[1])
        elif self.player.feet.colliderect(self.map_manager.panneau_3_rect) :
            self.status = self.DIALOG_MODE
            self.dialog_box.execute(self.dialog_box.dialogs[2])
        for door in self.map_manager.doors :
            if self.player.feet.colliderect(door) :
                self.status = self.DIALOG_MODE
                self.dialog_box.execute(self.dialog_box.dialogs[3])
        if self.player.feet.colliderect(self.map_manager.boite_aux_lettres_rect) :
            self.status = self.DIALOG_MODE
            self.dialog_box.execute(self.dialog_box.dialogs[4])
        elif self.player.feet.colliderect(self.map_manager.panneau_explicatif_rect) :
            self.status = self.DIALOG_MODE
            self.dialog_box.execute(self.dialog_box.dialogs[5])
        elif self.player.feet.colliderect(self.map_manager.quest_board_rect) :
            if len(self.map_manager.keys_collected) == 11 :
                self.dialog_box.execute(self.dialog_box.dialogs[8])
            else :
                self.status = self.DIALOG_MODE
                self.dialog_box.execute(self.dialog_box.dialogs[6])
        for key in self.map_manager.keys :
            if self.player.feet.colliderect(pygame.Rect(key.x, key.y, key.width, key.height)) :
                self.status = self.DIALOG_MODE
                if len(self.map_manager.keys_collected) == self.map_manager.nb_keys-1 :
                    self.dialog_box.execute(self.dialog_box.dialogs[8])
                elif len(self.map_manager.keys_collected) < self.map_manager.nb_keys-1 :
                    self.dialog_box.execute(["Vous prenez la clé. Encore " + str(len(self.map_manager.keys) - 1) + " à récupérer."])
                    if not self.map_manager.contains(key, self.map_manager.keys_collected) :
                        self.map_manager.keys_collected.append(key)
                
                
    def run(self) :
        """Lance le jeu à l'aide des méthodes de la classe game et gère sa fermeture"""
        #generation de la musique
        self.music = pygame.mixer.Sound("soundtrack/world_music.ogg")
        self.music.play(-1, 0, 5000)
        
        #boucle du jeu
        while self.running :
            
            self.player.save_location()
            if self.status == self.ADVENTURE_MODE :
                for obtained in self.map_manager.keys_collected :
                    if self.map_manager.contains(obtained, self.map_manager.keys) :
                        self.map_manager.keys.remove(obtained)
                self.handle_input()
            self.update()
            self.map_manager.draw()
            if self.status == self.DIALOG_MODE :
                self.dialog_box.render_slow(self.screen)
                if self.dialog_box.end_text :
                    self.status = self.ADVENTURE_MODE
                    self.dialog_box.end_text = False
            pygame.display.flip()
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_e :
                        self.check()
                    if len(self.map_manager.keys_collected) == 11 :
                        self.status = self.DIALOG_MODE
                        self.dialog_box.execute(self.dialog_box.dialogs[7])
            self.clock.tick(120)
        #ferme la fenêtre
        self.music.stop()
        pygame.quit()
