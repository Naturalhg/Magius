import pygame
from game import Game # récupère la classe Game()

if __name__ == '__main__' :
    pygame.init() # initialise le module pygame
    game = Game() # attribue la classe Game() à game
    game.run() # active la boucle du jeu