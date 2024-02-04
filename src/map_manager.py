from dataclasses import dataclass
import pygame, pytmx, pyscroll

@dataclass
class Portal :
    origin_world: str
    collide_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map :
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    
class Map_Manager :
    def __init__(self, screen, player) :
        self.maps = dict() # permet de récupérer les éléments d'un monde
        self.screen = screen
        self.player = player
        self.current_map = "world"
        
        self.register_map("world", 2, portals=[
            Portal("world", "enter_house", "inside_house", "spawn_house"),
            Portal("world", "enter_tree_house", "tree_house", "spawn_tree_house"),
            Portal("world", "enter_market1", "market1", "spawn_market1"),
            Portal("world", "enter_market2", "market2", "spawn_market2"),
            Portal("world", "enter_town_hall", "town_hall", "spawn_town_hall")
            ])
        self.register_map("inside_house", 4, portals=[Portal("inside_house", "exit_house", "world", "enter_house_exit")])
        self.register_map("tree_house", 4, portals=[Portal("tree_house", "exit_tree_house", "world", "enter_tree_house_exit")])
        self.register_map("market1", 4, portals=[Portal("market1", "exit_market1", "world", "enter_market1_exit")])
        self.register_map("market2", 4, portals=[Portal("market2", "exit_market2", "world", "enter_market2_exit")])
        self.register_map("town_hall", 4, portals=[Portal("town_hall", "exit_town_hall", "world", "enter_town_hall_exit")])
        
        self.teleport_player("spawn_start")
        
        self.nb_keys = 11
        self.keys = []
        self.keys_collected = []
        """définition des clés"""
        #récupération des différents lieux qui contiennent des clés
        tmx_data = pytmx.util_pygame.load_pygame('map//world.tmx')
        tmx_data_tree_h = pytmx.util_pygame.load_pygame('map/tree_house.tmx')
        tmx_data_inside_h = pytmx.util_pygame.load_pygame('map/inside_house.tmx')
        tmx_data_market1 = pytmx.util_pygame.load_pygame('map/market1.tmx')
        tmx_data_market2 = pytmx.util_pygame.load_pygame('map/market2.tmx')
        tmx_data_town_hall = pytmx.util_pygame.load_pygame('map/town_hall.tmx')
        
        #ajout de toutes les clés
        self.add_keys(tmx_data)
        self.add_keys(tmx_data_inside_h)
        self.add_keys(tmx_data_tree_h)
        self.add_keys(tmx_data_market1)
        self.add_keys(tmx_data_market2)
        self.add_keys(tmx_data_town_hall)
    
    def add_keys(self, tmx_data) :
        """Ajoute toutes les clés d'une carte dans self.keys"""
        for objet in tmx_data.objects :
            if objet.type == 'key' :
                if self.keys_collected != [] :
                    if self.contains(objet, self.keys_collected) :
                        break
                if self.keys != [] :
                    if self.contains(objet, self.keys) :
                        break
                self.keys.append(objet) # ajoute la clé à la liste des clés
    
    def contains(self, objet, liste) :
        """Renvoie True si l'objet est dans la liste donnée et False sinon"""
        for element in liste :
            if objet == element :
                return True
        return False
    
    def check_collisions(self) :
        """Détecte les différentes collisions et applique l'effet adapté"""
        
        #détection des collisions avec les portails
        for portal in self.get_map().portals :
            if portal.origin_world == self.current_map:
                point = self.get_object(portal.collide_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                
                if self.player.feet.colliderect(rect) :
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
        
        #détection des collision avec les murs
        for sprite in self.get_group().sprites() :
            if sprite.feet.collidelist(self.get_walls()) > -1 :
                sprite.move_back()
    
    def teleport_player(self, name) :
        spawn = self.get_object(name)
        self.player.position[0] = spawn.x
        self.player.position[1] = spawn.y
        self.player.save_location()
    
    def register_map(self, name, zoom, portals=[]) :
        """Actualise le monde sur la map """
        
        #generation de la carte et règle son zoom
        tmx_data = pytmx.util_pygame.load_pygame(f'map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = zoom
        
        #generation des collisions
        walls = []
        for objet in tmx_data.objects :
            if objet.type == 'collision' :
                walls.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        
        if name == 'world' :
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
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 7)
        group.add(self.player)
        
        #crée un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals)
        
    def get_map(self) :
        return self.maps[self.current_map]
    
    def get_group(self) :
        return self.get_map().group
    
    def get_walls(self) :
        return self.get_map().walls
    
    def get_object(self, name) :
        return self.get_map().tmx_data.get_object_by_name(name)
    
    def draw(self) :
        self.get_group().center(self.player.rect.center)
        self.get_group().draw(self.screen)
    
    def update(self) :
        self.get_group().update()
        self.check_collisions()