import pygame, pytmx, pyscroll

from player import Player

class Worlds() :
    
    def __init__(self) :
        self.keys = []
        self.keys_collected = []
        
        #crée la fenêtre du jeu
        self.screen = pygame.display.set_mode((1350, 700)) #taille
        pygame.display.set_caption("Magius")  #titre
        
        self.player = Player(0,0)
    
    
    def add_keys(self, tmx_data) :
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                if self.keys_collected != [] :
                    if self.contains(objet, self.keys_collected) :
                        break
                if self.keys != [] :
                    if self.contains(objet, self.keys) :
                        break
                self.keys.append(objet) # ajoute la clé à la liste des clés
    
    def contains(self, object, tab) :
        for element in tab :
            if object == element :
                return True
    
    
    
    def switch_world(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        #generation de la musique
        self.music = pygame.mixer.Sound("../soundtrack/world_music.ogg")
        self.music.play(-1, 0, 5000)
        
        #generation du joueur
        player_position = tmx_data.get_object_by_name('spawn_start')
        self.player = Player(player_position.x, player_position.y)
        
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
        
        """définition des clés"""
        #récupération des différents lieux qui contiennent des clés
        tmx_data_tree_h = pytmx.util_pygame.load_pygame('../map//tree_house.tmx')
        tmx_data_inside_h = pytmx.util_pygame.load_pygame('../map/inside_house.tmx')
        tmx_data_market1 = pytmx.util_pygame.load_pygame('../map/market1.tmx')
        tmx_data_market2 = pytmx.util_pygame.load_pygame('../map/market2.tmx')
        tmx_data_town_hall = pytmx.util_pygame.load_pygame('../map//town_hall.tmx')
        
        #ajout de toutes les clés
        self.add_keys(tmx_data)
        self.add_keys(tmx_data_inside_h)
        self.add_keys(tmx_data_tree_h)
        self.add_keys(tmx_data_market1)
        self.add_keys(tmx_data_market2)
        self.add_keys(tmx_data_town_hall)
        
        
    def switch_world_house(self) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
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
        
        #definir le rect pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #récupère le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 10

    
    
    def switch_house(self) :
        """Actualise le monde sur la maison """
        
        tmx_data = pytmx.util_pygame.load_pygame('../map/inside_house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
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
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
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
        
        #definir le rect pour entrer dans la cabane
        enter_tree_house = tmx_data.get_object_by_name('enter_tree_house')
        self.enter_tree_house_rect = pygame.Rect(enter_tree_house.x, enter_tree_house.y, enter_tree_house.width, enter_tree_house.height)
        
        #récupère le point de spawn devant la cabane
        spawn_tree_house_point = tmx_data.get_object_by_name('enter_tree_house_exit')
        self.player.position[0] = spawn_tree_house_point.x
        self.player.position[1] = spawn_tree_house_point.y + 10

    
    
    def switch_tree_house(self) :
        """Actualise le monde sur la cabane """
        
        tmx_data = pytmx.util_pygame.load_pygame('../map//tree_house.tmx')
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
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
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
        
        #definir le rect pour entrer dans la magasin1
        enter_market1 = tmx_data.get_object_by_name('enter_market1')
        self.enter_market1_rect = pygame.Rect(enter_market1.x, enter_market1.y, enter_market1.width, enter_market1.height)
    
        #récupère le point de spawn devant le magasin1
        spawn_market1_point = tmx_data.get_object_by_name('enter_market1_exit')
        self.player.position[0] = spawn_market1_point.x
        self.player.position[1] = spawn_market1_point.y + 10
    
    
    
    def switch_market1(self) :
        """Actualise le monde sur le magasin1 """
        
        tmx_data = pytmx.util_pygame.load_pygame('../map/market1.tmx')
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
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
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
        
        #definir le rect pour entrer dans la magasin2
        enter_market2 = tmx_data.get_object_by_name('enter_market2')
        self.enter_market2_rect = pygame.Rect(enter_market2.x, enter_market2.y, enter_market2.width, enter_market2.height)

        #récupère le point de spawn devant le magasin2
        spawn_market2_point = tmx_data.get_object_by_name('enter_market2_exit')
        self.player.position[0] = spawn_market2_point.x
        self.player.position[1] = spawn_market2_point.y + 10
    
    
    
    def switch_market2(self) :
        """Actualise le monde sur le magasin2 """
        
        tmx_data = pytmx.util_pygame.load_pygame('../map/market2.tmx')
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
        tmx_data = pytmx.util_pygame.load_pygame('../map/map.tmx')
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
        
        #definir le rect pour entrer dans la mairie
        enter_town_hall = tmx_data.get_object_by_name('enter_town_hall')
        self.enter_town_hall_rect = pygame.Rect(enter_town_hall.x, enter_town_hall.y, enter_town_hall.width, enter_town_hall.height)

        #récupère le point de spawn devant la mairie
        spawn_town_hall_point = tmx_data.get_object_by_name('enter_town_hall_exit')
        self.player.position[0] = spawn_town_hall_point.x
        self.player.position[1] = spawn_town_hall_point.y + 10
    
    
    
    def switch_town_hall(self) :
        """Actualise le monde sur la mairie """
        
        tmx_data = pytmx.util_pygame.load_pygame('../map//town_hall.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3
        
        #generation des collisions
        self.walls = [] # liste qui contient toutes les collisions
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                self.walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height)) # ajoute l'objet à la liste des murs
        
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
    