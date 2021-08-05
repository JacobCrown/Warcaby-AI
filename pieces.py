import pygame
from pygame.locals import *
from constants import *

# Klasa Piece realizująca piona na planszy 
class Piece(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.queen = False
        self.possibleMoves = []
        self.possibleKillMoves = {}

    # metoda rysująca piona na zadanej powierzchnii
    def drawPiece(self, window):
        pygame.draw.circle(window, self.color, ((self.x - 1) * SIZE + SIZE//2, (self.y - 1) * SIZE + SIZE//2), SIZE//2 - 8)
        if self.queen == True:
            big_img = pygame.image.load(r'Photos\star.png')
            img = pygame.transform.smoothscale(big_img, (40,40))
            window.blit(img, ((self.x - 1) * SIZE + SIZE // 2 - img.get_width()//2, (self.y - 1) * SIZE + SIZE // 2 - img.get_height()//2))
            
        
    # funkcja sprawdzająca czy dany ruch jest możliwy
    def checkIfMoveIsPossible(self, x, y):
        for move in self.possibleMoves:
            if move[0] == x and move[1] == y:
                return True
        return False
    
    # funkcja sprawdzająca czy bicie jest możliwe
    def checkIfKillIsPossible(self, x, y):
        for move in self.possibleKillMoves:
            if move[0] == x and move[1] == y:
                return True
        return False
    
    # funkcja przemieszczająca piona na dane koordynaty na planszy
    def move(self, x, y):
        self.x = x
        self.y = y
    
    # funkcja pomocna przy biciu przeciwnika
    def killMove(self, x, y):
        self.x = x
        self.y = y
        self.possibleKillMoves.pop(x,y)
        
    # funkcja sprawdza czy pion jest damką. Jeśli tak to zwraca True, jeśli nie to False
    def isQueen(self):
        if self.queen == False:
            return False
        else:
            return True
    
    # funkcja czyszcząca listę możliwych ruchów piona

    def clearAllMoves(self):
        self.possibleMoves.clear()
        self.possibleKillMoves.clear()


