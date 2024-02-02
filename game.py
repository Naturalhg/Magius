import pygame

from dialog import Dialog_box
from worlds import Worlds

pygame.init()

class Game() :
    
    ADVENTURE_MODE = 0
    DIALOG_MODE = 1
    
    def __init__(self) :
        self.dialog_box = Dialog_box()
        self.world = Worlds()
        self.clock = pygame.time.Clock()
        self.running = True
        self.map = 'map'
        self.status = 0
        self.dialogs = [["^ : Maison", "> : Village", "v : Forêt"], #panneau 1
                        ["^ : Cabane", "< : Maison", "> : Village"], #panneau 2
                        ["^ : Cimetière", "< : Maison", "> : Fontaine", "v : Village"], #panneau 3
                        ["Cette porte est fermée,", "quelqu'un habite ici."], #portes village
                        ["Il n'y a rien dans la boîte aux lettres."], #boîte aux lettres
                        ["Bienvenue dans notre monde,", "découvre ce monde par toi même en t'aidant", "des panneaux et accomplis la quête principale.", "Plus d'informations dans le tableau au village."], #panneau d'introduction
                        ["Quête principale :", "Récupérez les 11 clés réparties sur la carte."],
                        ["Bien joué ! Vous avez trouvé toutes les clés", "Plus de missions seront disponibles prochainement.", "Merci d'avoir joué à notre jeu."],
                        ["Vous avez trouvé toutes les clés !", "Que peuvent-elles bien ouvrir..."]
                        ]
    
    
    
    def handle_input(self) :
        """Indique le bouton pressé par l'utilisateur et déplace le joueur en conséquence"""
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_z] and pressed[pygame.K_SPACE] or pressed[pygame.K_UP] and pressed[pygame.K_SPACE]: # si 'z' et 'x' sont appuyés :
            self.world.player.speed_move_up()                  # méthode 'speed_move_up()' de la classe player
            self.world.player.change_animation('up')           # changement de l'animation 'up'
        elif pressed[pygame.K_s] and pressed[pygame.K_SPACE] or pressed[pygame.K_DOWN] and pressed[pygame.K_SPACE]:
            self.world.player.speed_move_down()
            self.world.player.change_animation('down')
        elif pressed[pygame.K_q] and pressed[pygame.K_SPACE] or pressed[pygame.K_LEFT] and pressed[pygame.K_SPACE]:
            self.world.player.speed_move_left()
            self.world.player.change_animation('left')
        elif pressed[pygame.K_d] and pressed[pygame.K_SPACE] or pressed[pygame.K_RIGHT] and pressed[pygame.K_SPACE]:
            self.world.player.speed_move_right()
            self.world.player.change_animation('right')
        
        elif pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.world.player.move_up()
            self.world.player.change_animation('up')
        elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.world.player.move_down()
            self.world.player.change_animation('down')
        elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.world.player.move_left()
            self.world.player.change_animation('left')
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.world.player.move_right()
            self.world.player.change_animation('right')
    
    def update(self) :
        """Actualise les sprites en fonction des collisions"""
        
        #verif sortie maison
        if self.map == 'map' and self.world.player.feet.colliderect(self.world.enter_house_rect) :
            self.world.switch_house()
            self.map = 'inside_house'
        
        #verif entrée maison
        if self.map == 'inside_house' and self.world.player.feet.colliderect(self.world.enter_house_rect) :
            self.world.switch_world_house()
            self.map = 'map'
        
        #verif sortie cabane
        if self.map == 'map' and self.world.player.feet.colliderect(self.world.enter_tree_house_rect) :
            self.world.switch_tree_house()
            self.map = 'tree_house'
            
        #verif entrée cabane
        if self.map == 'tree_house' and self.world.player.feet.colliderect(self.world.enter_tree_house_rect) :
            self.world.switch_world_tree_house()
            self.map = 'map'
            
        #verif sortie magasin1
        if self.map == 'map' and self.world.player.feet.colliderect(self.world.enter_market1_rect) :
            self.world.switch_market1()
            self.map = 'market1'
            
        #verif entrée magasin1
        if self.map == 'market1' and self.world.player.feet.colliderect(self.world.enter_market1_rect) :
            self.world.switch_world_market1()
            self.map = 'map'
            
        #verif sortie magasin2
        if self.map == 'map' and self.world.player.feet.colliderect(self.world.enter_market2_rect) :
            self.world.switch_market2()
            self.map = 'market2'
            
        #verif entrée magasin2
        if self.map == 'market2' and self.world.player.feet.colliderect(self.world.enter_market2_rect) :
            self.world.switch_world_market2()
            self.map = 'map'
            
        #verif sortie mairie
        if self.map == 'map' and self.world.player.feet.colliderect(self.world.enter_town_hall_rect) :
            self.world.switch_town_hall()
            self.map = 'town_hall'
            
        #verif entrée mairie
        if self.map == 'town_hall' and self.world.player.feet.colliderect(self.world.enter_town_hall_rect) :
            self.world.switch_world_town_hall()
            self.map = 'map'
        
        #verif des collisions
        self.world.group.update()
        for sprite in self.world.group.sprites() :
            if sprite.feet.collidelist(self.world.walls) > -1 :
                sprite.move_back()
    
    def check(self, dialog_box) :
        """Affiche le texte correspondant à l'objet rencontré"""
        if self.world.player.feet.colliderect(self.world.panneau_1_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[0])
        elif self.world.player.feet.colliderect(self.world.panneau_2_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[1])
        elif self.world.player.feet.colliderect(self.world.panneau_3_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[2])
        for door in self.world.doors :
            if self.world.player.feet.colliderect(door) :
                self.status = self.DIALOG_MODE
                dialog_box.execute(self.dialogs[3])
        if self.world.player.feet.colliderect(self.world.boite_aux_lettres_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[4])
        elif self.world.player.feet.colliderect(self.world.panneau_explicatif_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[5])
        elif self.world.player.feet.colliderect(self.world.quest_board_rect) :
            if len(self.world.keys_collected) == 11 :
                dialog_box.execute(self.dialogs[8])
            else :
                self.status = self.DIALOG_MODE
                dialog_box.execute(self.dialogs[6])
        for key in self.world.keys :
            if self.world.player.feet.colliderect(pygame.Rect(key.x, key.y, key.width, key.height)) :
                self.status = self.DIALOG_MODE
                if len(self.world.keys_collected) == 10 :
                    dialog_box.execute(self.dialogs[8])
                elif len(self.world.keys_collected) < 10 :
                    dialog_box.execute(["Vous prenez la clé. Encore " + str(len(self.world.keys) - 1) + " à récupérer."])
                    if not self.world.contains(key, self.world.keys_collected) :
                        self.world.keys_collected.append(key)
                else :
                    dialog_box.execute(["Key not found"])
                
                
    def run(self) :
        """Lance le jeu à l'aide des méthodes de la classe game et gère sa fermeture"""
        self.world.switch_world()
        
        #boucle du jeu
        while self.running :
            
            self.world.player.save_location()
            if self.status == self.ADVENTURE_MODE :
                for obtained in self.world.keys_collected :
                    if self.world.contains(obtained, self.world.keys) :
                        self.world.keys.remove(obtained)
                self.handle_input()
            self.update()
            self.world.group.center(self.world.player.rect.center)
            self.world.group.draw(self.world.screen)
            if self.status == self.DIALOG_MODE :
                self.dialog_box.render_slow(self.world.screen)
                if self.dialog_box.end_text :
                    self.status = self.ADVENTURE_MODE
                    self.dialog_box.end_text = False
            pygame.display.flip()
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_e :
                        self.check(self.dialog_box)
                    if len(self.world.keys_collected) == 11 :
                        self.status = self.DIALOG_MODE
                        self.dialog_box.execute(self.dialogs[7])
            self.clock.tick(120)
        #ferme la fenêtre
        self.world.music.stop()
        pygame.quit()
