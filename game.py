import pygame, pytmx, pyscroll, time
from player import Player
from dialog import Dialog_box

pygame.init()

class Game() :
    
    ADVENTURE_MODE = 0
    DIALOG_MODE = 1
    
    def __init__(self) :
        self.clock = pygame.time.Clock()
        self.running = True
        self.map = 'map'
        self.sprite_sheet = pygame.image.load("aventurier_1.png")
        self.key_founded = 0
        self.nb_keys = 11
        self.status = 0
        self.keys = []
        self.keys_collected = []
        self.current_key = []
        self.dialogs = [["^ : Maison", "> : Village", "v : Forêt"], #panneau 1
                        ["^ : Cabane", "< : Maison", "> : Village"], #panneau 2
                        ["^ : Cimetière", "< : Maison", "> : Fontaine", "v : Village"], #panneau 3
                        ["Cette porte est fermée,", "quelqu'un habite ici."], #portes village
                        ["Il n'y a rien dans la boîte aux lettres."], #boîte aux lettres
                        ["Bienvenue dans notre monde,", "découvre ce monde par toi même en t'aidant", "des panneaux et accomplis la quête principale.", "Plus d'informations sur le tableau du village."], #panneau d'introduction
                        ["Quête principale :", "Récupérez les 11 clés réparties sur la carte."],
                        ["Bien joué ! Vous avez trouvé toutes les clés", "Plus de missions seront disponibles prochainement.", "Merci d'avoir joué à notre jeu."]
                        ]
        
        #crée la fenêtre du jeu
        self.screen = pygame.display.set_mode((1350, 700)) #taille
        pygame.display.set_caption('Magius')  #titre
    
    def switch_world(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        #generation de la musique
        self.music = pygame.mixer.Sound("world_music.ogg")
        self.music.play(-1, 0, 5000)
        
        #generation du joueur
        player_position = tmx_data.get_object_by_name('spawn_start')
        self.player = Player(player_position.x, player_position.y)
        self.dialog_box = Dialog_box()
            
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
                
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #generation des objets interactifs du jeu
        panneau_1 = tmx_data.get_object_by_name('panneau_1')
        self.panneau_1_rect = pygame.Rect(panneau_1.x, panneau_1.y, panneau_1.width, panneau_1.height)
        
        panneau_2 = tmx_data.get_object_by_name('panneau_2')
        self.panneau_2_rect = pygame.Rect(panneau_2.x, panneau_2.y, panneau_2.width, panneau_2.height)
        
        panneau_3 = tmx_data.get_object_by_name('panneau_3')
        self.panneau_3_rect = pygame.Rect(panneau_3.x, panneau_3.y, panneau_3.width, panneau_3.height)
        
        boite_aux_lettres = tmx_data.get_object_by_name('boite_aux_lettres')
        self.boite_aux_lettres_rect = pygame.Rect(boite_aux_lettres.x, boite_aux_lettres.y, boite_aux_lettres.width, boite_aux_lettres.height)
        
        panneau_explicatif = tmx_data.get_object_by_name('panneau_explicatif')
        self.panneau_explicatif_rect = pygame.Rect(panneau_explicatif.x, panneau_explicatif.y, panneau_explicatif.width, panneau_explicatif.height)
                
        quest_board = tmx_data.get_object_by_name('quest_board')
        self.quest_board_rect = pygame.Rect(quest_board.x, quest_board.y, quest_board.width, quest_board.height)
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #definir le rect pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
            
        #definir le rect pour entrer dans la cabane
        enter_tree_house = tmx_data.get_object_by_name('enter_tree_house')
        self.enter_tree_house_rect = pygame.Rect(enter_tree_house.x, enter_tree_house.y, enter_tree_house.width, enter_tree_house.height)
        
        #definir le rect pour entrer dans le magasin1
        enter_market1 = tmx_data.get_object_by_name('enter_market1')
        self.enter_market1_rect = pygame.Rect(enter_market1.x, enter_market1.y, enter_market1.width, enter_market1.height)
        
        #definir le rect pour entrer dans le magasin2
        enter_market2 = tmx_data.get_object_by_name('enter_market2')
        self.enter_market2_rect = pygame.Rect(enter_market2.x, enter_market2.y, enter_market2.width, enter_market2.height)
        
        #definir le rect pour entrer dans la mairie
        enter_town_hall = tmx_data.get_object_by_name('enter_town_hall')
        self.enter_town_hall_rect = pygame.Rect(enter_town_hall.x, enter_town_hall.y, enter_town_hall.width, enter_town_hall.height)
        
        #définition des clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
                """
                key = pygame.Rect(objet.x, objet.y, objet.width, objet.height)
                index = 0
                for i in self.keys_collected :
                    if key == i :
                        index += 1
                    elif index == len(self.keys_collected) :
                        self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
                """
                        
        self.keys_copy = self.keys #copie la liste des clés
        
    def switch_world_house(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
           
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
                
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
                    
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #definir le rect pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
    
        #récupère le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 10
    
    def switch_house(self) :
        """Actualise le monde sur la maison """
        
        tmx_data = pytmx.util_pygame.load_pygame('inside_house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7) # definit la position du calque player
        self.group.add(self.player) # ajoute le player comme un calque Tiled

        #definir le rect pour sortir de la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        
        #récupère le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('exit_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 40 # permet d'éviter de spawn sur l'entrée (enter_house) de la maison
    
    def switch_world_tree_house(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
                
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
                    
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #definir le rect pour entrer dans la cabane
        enter_tree_house = tmx_data.get_object_by_name('enter_tree_house')
        self.enter_tree_house_rect = pygame.Rect(enter_tree_house.x, enter_tree_house.y, enter_tree_house.width, enter_tree_house.height)
    
        #récupère le point de spawn devant la cabane
        spawn_tree_house_point = tmx_data.get_object_by_name('enter_tree_house_exit')
        self.player.position[0] = spawn_tree_house_point.x
        self.player.position[1] = spawn_tree_house_point.y + 10
    
    def switch_tree_house(self) :
        """Actualise le monde sur la cabane """
        
        tmx_data = pytmx.util_pygame.load_pygame('tree_house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 0) # definit la position du calque player
        self.group.add(self.player) # ajoute le player comme un calque Tiled
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #definir le rect pour sortir de la cabane
        enter_tree_house = tmx_data.get_object_by_name('exit_tree_house')
        self.enter_tree_house_rect = pygame.Rect(enter_tree_house.x, enter_tree_house.y, enter_tree_house.width, enter_tree_house.height)
        
        #récupère le point de spawn devant la cabane
        spawn_tree_house_point = tmx_data.get_object_by_name('exit_tree_house')
        self.player.position[0] = spawn_tree_house_point.x
        self.player.position[1] = spawn_tree_house_point.y - 40 # permet d'éviter de spawn sur l'entrée (enter_tree_house) de la cabane
        
    def switch_world_market1(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
           
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
                
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #definir le rect pour entrer dans la magasin1
        enter_market1 = tmx_data.get_object_by_name('enter_market1')
        self.enter_market1_rect = pygame.Rect(enter_market1.x, enter_market1.y, enter_market1.width, enter_market1.height)
    
        #récupère le point de spawn devant le magasin1
        spawn_market1_point = tmx_data.get_object_by_name('enter_market1_exit')
        self.player.position[0] = spawn_market1_point.x
        self.player.position[1] = spawn_market1_point.y + 10
        
    def switch_market1(self) :
        """Actualise le monde sur le magasin1 """
        
        tmx_data = pytmx.util_pygame.load_pygame('market1.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 0) # definit la position du calque player
        self.group.add(self.player) # ajoute le player comme un calque Tiled

        #definir le rect pour sortir de le magasin1
        enter_market1 = tmx_data.get_object_by_name('exit_market1')
        self.enter_market1_rect = pygame.Rect(enter_market1.x, enter_market1.y, enter_market1.width, enter_market1.height)
        
        #récupère le point de spawn devant le magasin1
        spawn_market1_point = tmx_data.get_object_by_name('exit_market1')
        self.player.position[0] = spawn_market1_point.x
        self.player.position[1] = spawn_market1_point.y - 40 # permet d'éviter de spawn sur l'entrée (enter_market1) de la cabane
        
    def switch_world_market2(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
       
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
                
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #definir le rect pour entrer dans la magasin2
        enter_market2 = tmx_data.get_object_by_name('enter_market2')
        self.enter_market2_rect = pygame.Rect(enter_market2.x, enter_market2.y, enter_market2.width, enter_market2.height)
    
        #récupère le point de spawn devant le magasin2
        spawn_market2_point = tmx_data.get_object_by_name('enter_market2_exit')
        self.player.position[0] = spawn_market2_point.x
        self.player.position[1] = spawn_market2_point.y + 10    
        
    def switch_market2(self) :
        """Actualise le monde sur le magasin2 """
        
        tmx_data = pytmx.util_pygame.load_pygame('market2.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 0) # definit la position du calque player
        self.group.add(self.player) # ajoute le player comme un calque Tiled

        #definir le rect pour sortir de le magasin2
        enter_market2 = tmx_data.get_object_by_name('exit_market2')
        self.enter_market2_rect = pygame.Rect(enter_market2.x, enter_market2.y, enter_market2.width, enter_market2.height)
        
        #récupère le point de spawn devant le magasin2
        spawn_market2_point = tmx_data.get_object_by_name('exit_market2')
        self.player.position[0] = spawn_market2_point.x
        self.player.position[1] = spawn_market2_point.y - 40 # permet d'éviter de spawn sur l'entrée (enter_market2) de la cabane
        
    def switch_world_town_hall(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
       
        #generation des collisions
        self.walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
            
        #generation des portes fermées
        self.doors = []
        for objet in tmx_data.objects :
            if objet.type == 'closed_door' :
                self.doors.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
        
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        self.group.add(self.player)
        
        #definir le rect pour entrer dans la mairie
        enter_town_hall = tmx_data.get_object_by_name('enter_town_hall')
        self.enter_town_hall_rect = pygame.Rect(enter_town_hall.x, enter_town_hall.y, enter_town_hall.width, enter_town_hall.height)
    
        #récupère le point de spawn devant la mairie
        spawn_town_hall_point = tmx_data.get_object_by_name('enter_town_hall_exit')
        self.player.position[0] = spawn_town_hall_point.x
        self.player.position[1] = spawn_town_hall_point.y + 10
        
    def switch_town_hall(self) :
        """Actualise le monde sur la mairie """
        
        tmx_data = pytmx.util_pygame.load_pygame('town_hall.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
        #définition des clés
        self.keys = [] # liste qui contient toutes les clés
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                self.keys.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des clés
        self.keys_copy = self.keys #copie la liste des clés
            
        #dessin du groupe et calques
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 5) # definit la position du calque player
        self.group.add(self.player) # ajoute le player comme un calque Tiled

        #definir le rect pour sortir de la mairie
        enter_town_hall = tmx_data.get_object_by_name('exit_town_hall')
        self.enter_town_hall_rect = pygame.Rect(enter_town_hall.x, enter_town_hall.y, enter_town_hall.width, enter_town_hall.height)
        
        #récupère le point de spawn devant la mairie
        spawn_town_hall_point = tmx_data.get_object_by_name('exit_town_hall')
        self.player.position[0] = spawn_town_hall_point.x
        self.player.position[1] = spawn_town_hall_point.y - 40 # permet d'éviter de spawn sur l'entrée (enter_town_hall) de la cabane
        
        
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
        
        #verif sortie maison
        if self.map == 'map' and self.player.feet.colliderect(self.enter_house_rect) :
            self.switch_house()
            self.map = 'inside_house'
            
        #verif entrée maison
        if self.map == 'inside_house' and self.player.feet.colliderect(self.enter_house_rect) :
            self.switch_world_house()
            self.map = 'map'
        
        #verif sortie cabane
        if self.map == 'map' and self.player.feet.colliderect(self.enter_tree_house_rect) :
            self.switch_tree_house()
            self.map = 'tree_house'
            
        #verif entrée cabane
        if self.map == 'tree_house' and self.player.feet.colliderect(self.enter_tree_house_rect) :
            self.switch_world_tree_house()
            self.map = 'map'
            
        #verif sortie magasin1
        if self.map == 'map' and self.player.feet.colliderect(self.enter_market1_rect) :
            self.switch_market1()
            self.map = 'market1'
            
        #verif entrée magasin1
        if self.map == 'market1' and self.player.feet.colliderect(self.enter_market1_rect) :
            self.switch_world_market1()
            self.map = 'map'
            
        #verif sortie magasin2
        if self.map == 'map' and self.player.feet.colliderect(self.enter_market2_rect) :
            self.switch_market2()
            self.map = 'market2'
            
        #verif entrée magasin2
        if self.map == 'market2' and self.player.feet.colliderect(self.enter_market2_rect) :
            self.switch_world_market2()
            self.map = 'map'
            
        #verif sortie mairie
        if self.map == 'map' and self.player.feet.colliderect(self.enter_town_hall_rect) :
            self.switch_town_hall()
            self.map = 'town_hall'
            
        #verif entrée mairie
        if self.map == 'town_hall' and self.player.feet.colliderect(self.enter_town_hall_rect) :
            self.switch_world_town_hall()
            self.map = 'map'
        
        #verif des collisions
        self.group.update()
        for sprite in self.group.sprites() :
            if sprite.feet.collidelist(self.walls) > -1 :
                sprite.move_back()
    
    def check(self, dialog_box) :
        """Affiche le texte correspondant à l'objet rencontré"""
        if self.player.feet.colliderect(self.panneau_1_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[0])
        elif self.player.feet.colliderect(self.panneau_2_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[1])
        elif self.player.feet.colliderect(self.panneau_3_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[2])
        for door in self.doors :
            if self.player.feet.colliderect(door) :
                self.status = self.DIALOG_MODE
                dialog_box.execute(self.dialogs[3])
        if self.player.feet.colliderect(self.boite_aux_lettres_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[4])
        elif self.player.feet.colliderect(self.panneau_explicatif_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[5])
        elif self.player.feet.colliderect(self.quest_board_rect) :
            self.status = self.DIALOG_MODE
            dialog_box.execute(self.dialogs[6])
        for key in self.keys :
            if self.player.feet.colliderect(key) :
                self.status = self.DIALOG_MODE
                if self.nb_keys <= 1 :
                    dialog_box.execute(["Vous avez trouvé toutes les clés."])
                if self.nb_keys > 1 :
                    dialog_box.execute(["Vous prenez la clé. Encore " + str(round(self.nb_keys - 1)) + " à récupérer."])
                for key_copy in self.keys_copy :
                    if key_copy == key and self.nb_keys > 1 :
                        self.nb_keys -= 1/2
                        self.key_founded += 1/2
                        self.current_key = [key]
                
                
    def run(self) :
        """Lance le jeu à l'aide des méthodes de la classe game et gère sa fermeture"""
        self.switch_world()
        pressed = pygame.key.get_pressed()
        
        #boucle du jeu
        while self.running :
            
            self.player.save_location()
            if self.status == self.ADVENTURE_MODE :
                self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            if self.status == self.DIALOG_MODE :
                self.dialog_box.render_slow(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_e :
                        self.check(self.dialog_box)
                    elif self.dialog_box.end_text :
                        if self.current_key != [] :
                            self.keys.remove(self.current_key[0])
                            self.keys_collected.append(self.current_key[0])
                        self.current_key = []
                        self.status = self.ADVENTURE_MODE
                    elif self.nb_keys <= 1 and event.key == pygame.K_f :
                        self.status = self.DIALOG_MODE
                        self.dialog_box.execute(self.dialogs[7])
                        """
                        if self.dialog_box.end_text :
                            self.status = self.ADVENTURE_MODE
                        """
            self.clock.tick(120)
        #ferme la fenêtre
        self.music.stop()
        pygame.quit()
