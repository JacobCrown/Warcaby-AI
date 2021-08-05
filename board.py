import pygame
from constants import *
from pieces import Piece


# klasa reprezentująca planszę
class Board(object):
    def __init__(self, color1player, color2player, color1square, color2square, width = 8, height = 8):
        self.color1player = color1player
        self.color1square = color1square
        self.color2player = color2player
        self.color2square = color2square
        self.width = width
        self.height = height
        self.player1pieces = []
        self.player2pieces = []
        self.turn = 1       # or self.turn = 2 when it's second player's turn
        self.killStreak = [False, None] # czy jest killStreak, oraz jakim pionem należy ten killStreak wykonać
        
        
    # funkcja rysująca planszę
    def drawBoard(self, window, piece):
        colorList = [self.color1square, self.color2square, self.color1square]
        for column in range(self.width):
            for row in range(self.height):
                pygame.draw.rect(window, colorList[row % 2 + column % 2], (SIZE * column, SIZE * row, SIZE, SIZE))
                
        for piece1p in self.player1pieces:
            piece1p.drawPiece(window)
        
        for piece2p in self.player2pieces:
            piece2p.drawPiece(window)
            
        if piece != None :
            # self.drawAllPossiblePieceMoves(window, piece)
            if piece in self.player2pieces:
                self.drawAllPossiblePieceMoves(window, piece)
                
    # funkcja pokazywania jakie są możliwe ruchy danego piona
    def drawAllPossiblePieceMoves(self, window, piece):
        for move in piece.possibleMoves:
            pygame.draw.circle(window, POSSIBLE_COLOR_MOVE, ((move[0] - 1) * SIZE + SIZE//2, (move[1] - 1) * SIZE + SIZE//2), SIZE//2 - 30)
        for killMove in piece.possibleKillMoves:
            pygame.draw.circle(window, POSSIBLE_COLOR_MOVE, ((killMove[0] - 1) * SIZE + SIZE//2, (killMove[1] - 1) * SIZE + SIZE//2), SIZE//2 - 30)
            
    # funkcja inicjalizująca planszę pionami
    def initializePieces(self):
        for i in range(1,4,2):
            for j in range(1,8,2):
                self.player1pieces.append(Piece(j, i, COLOR1P))
        for i in range(2,9,2):
            self.player1pieces.append(Piece(i, 2, COLOR1P))
                
        for i in range(6,9,2):
            for j in range(2,9,2):
                self.player2pieces.append(Piece(j, i, COLOR2P))
        for i in range(1,8,2):
            self.player2pieces.append(Piece(i, 7, COLOR2P))  
            
         
    # funkcja zwraca True gdy dane pole jest zajęte oraz False w przecinym razie
    def squareIsOccupied(self, x, y):
        if x < 1 or x > 8 or y < 1 or y > 8:
            return True
        
        
        for piece in self.player1pieces:
            if piece.x == x and piece.y == y:
                return True
    
        for piece in self.player2pieces:
            if piece.x == x and piece.y == y:
                return True
        return False
    
    # zwraca True gdy pole (x,y) jest zajęte przez przeciwnika
    def squareIsOccupiedByEnemy(self, x, y):       
        if self.turn == 1:
            for enemy in self.player2pieces:
                if enemy.x == x and enemy.y == y:
                    return True

        if self.turn == 2:
            for enemy in self.player1pieces:
                if enemy.x == x and enemy.y == y:
                    return True
        return False
            
    # funkcja dodaje wszystkie możliwe ruchy do listy możliwych ruchów pionów
    def getAllPossibleMoves(self):
        if self.turn == 1:
            for piece in self.player1pieces:
                piece.possibleMoves.clear()
                if piece.queen == False:
                    if not self.squareIsOccupied(piece.x + 1, piece.y + 1):
                        piece.possibleMoves.append([piece.x + 1, piece.y + 1])
                    if not self.squareIsOccupied(piece.x -1, piece.y + 1):
                        piece.possibleMoves.append([piece.x - 1, piece.y + 1])  
                else:   # gdy mamy doczynienia z damką
                    self.getAllQueensMoves(piece)
                    
                    
        if self.turn == 2:
            for piece in self.player2pieces:
                piece.possibleMoves.clear()
                if piece.queen == False:
                    if not self.squareIsOccupied(piece.x + 1, piece.y - 1):
                        piece.possibleMoves.append([piece.x + 1, piece.y - 1])
                    if not self.squareIsOccupied(piece.x -1, piece.y - 1):
                        piece.possibleMoves.append([piece.x - 1, piece.y - 1])  
                else:   # gdy mamy doczynienia z damką
                    self.getAllQueensMoves(piece) 
                    
                    
    # Sprawdzenie czy gra została zakończona
    def gameWon(self):
        
        if len(self.player1pieces) == 0 or len(self.player2pieces) == 0:
                return True
            
        
        if self.turn == 1:
            for piece in self.player1pieces:
                if len(piece.possibleMoves) > 0:
                    return False
                if len(piece.possibleKillMoves) > 0:
                    return False
        if self.turn == 2:
            for piece in self.player2pieces:
                if len(piece.possibleMoves) > 0:
                    
                    return False
                if len(piece.possibleKillMoves) > 0:
                    
                    return False
                
        return True
        
        

    # metoda dodająca możliwe ruchy damki do piece.possibleMoves
    def getAllQueensMoves(self, piece):
        (self.goTillSquareNotOccupied([1,1], piece, piece.x, piece.y ))
        (self.goTillSquareNotOccupied([-1,1], piece, piece.x, piece.y ))
        (self.goTillSquareNotOccupied([-1,-1], piece,piece.x, piece.y ))
        (self.goTillSquareNotOccupied([1,-1], piece,piece.x, piece.y ))
        
                
    # funkcja do obsługi ruchu damki o wiele pól
    def goTillSquareNotOccupied(self, vector, piece, x, y):
        if not self.squareIsOccupied(x + vector[0], y + vector[1]):
            piece.possibleMoves.append([x + vector[0], y + vector[1]])
            self.goTillSquareNotOccupied(vector, piece, x + vector[0], y + vector[1])


            
        

    
    # funkcja zwraca referencję do obiektu Piece występującego na pozycji (x,y)
    # Zwraca None gdy na tej pozycji nie ma żadnego piona
    def getPiece(self, x, y):
        if self.turn == 1:
            for piece in self.player1pieces:
                if piece.x == x and piece.y == y:
                    return piece
            return None
        if self.turn == 2:
            for piece in self.player2pieces:
                if piece.x == x and piece.y == y:
                    return piece
            return None
        
    # funkcja działa na tej samej zasadzie co poprzednia, jest przydatna przy zbijaniu 
    # pionów przeciwnika
    def getKillPiece(self, x, y):
        if self.turn == 1:
            for piece in self.player2pieces:
                if piece.x == x and piece.y == y:
                    return piece
            return None
        if self.turn == 2:
            for piece in self.player1pieces:
                if piece.x == x and piece.y == y:
                    return piece
            return None
    
    # funkcja usuwająca piona z listy
    def killPiece(self, piece):
        if self.turn == 1:
            self.player2pieces.remove(self.getKillPiece(piece[0], piece[1]))
            
        if self.turn == 2:
            
            self.player1pieces.remove(self.getKillPiece(piece[0], piece[1]))
    

    # zmienianie kolejki na drugiego przeciwnika    
    def toggleTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
    
    # funkcja dodaje do wszysktie możliwe ruchy do słownika możliwych ruchów, króre zbijają 
    # danego piona tworząc parę key-value, gdzie key to możliwy ruch, a value to pion przeciwnika,
    # który będzie zbity wykonując dany ruch 
    def getAllPossibleKills(self):
        
        if self.turn == 1:
            for piece in self.player1pieces:
                piece.possibleKillMoves.clear()
                if piece.queen == False:
                    listOfEnemies = self.enemiesNearby(piece)
                    for enemy in listOfEnemies:
                        self.checkIfKillPossible(piece, enemy)
                else:
                    listOfEnemies = self.queensEnemies(piece)
                    for enemy in listOfEnemies:
                        self.checkIfKillPossible(piece, enemy)
        
        if self.turn == 2:
            for piece in self.player2pieces:
                piece.possibleKillMoves.clear()
                if piece.queen == False:
                    listOfEnemies = self.enemiesNearby(piece)
                    for enemy in listOfEnemies:
                        self.checkIfKillPossible(piece, enemy)
                else:
                    listOfEnemies = self.queensEnemies(piece)
                    # # # print(listOfEnemies)
                    for enemy in listOfEnemies:
                        self.checkIfKillPossible(piece, enemy)
                    
        # for piece in self.player1pieces:
        #     print('Piece 1 :', piece.x , piece.y, 'moves:', piece.possibleMoves, "Kills:", piece.possibleKillMoves)   
            
        # for piece in self.player2pieces:
        #     print('Piece 2 :', piece.x , piece.y, 'moves:', piece.possibleMoves, "Kills:", piece.possibleKillMoves)   
            
        # print()
        # print()
        # print()

    # funkcja zwraca liczbę wrogich pionów w okolicy danego piona piece
    def enemiesNearby(self, piece):
        listOfEnemies = []
        if self.squareIsOccupiedByEnemy(piece.x + 1, piece.y + 1):
            listOfEnemies.append([piece.x + 1, piece.y + 1])
        if self.squareIsOccupiedByEnemy(piece.x - 1, piece.y + 1):
            listOfEnemies.append([piece.x - 1, piece.y + 1])
        if self.squareIsOccupiedByEnemy(piece.x - 1, piece.y - 1):
            listOfEnemies.append([piece.x - 1, piece.y - 1])
        if self.squareIsOccupiedByEnemy(piece.x + 1, piece.y - 1):
            listOfEnemies.append([piece.x + 1, piece.y - 1])
            # # print(piece.x, piece.y, listOfEnemies)
            
        return listOfEnemies
    
    # Funkcja zwraca koordynaty wrogich pionów na które patrzy damka
    def queensEnemies(self, piece):
        listOfEnemies = []
        
        listOfEnemies.append(self.goTillNearestEnemy([1, 1], piece.x, piece.y))
        listOfEnemies.append(self.goTillNearestEnemy([1, -1], piece.x, piece.y))
        listOfEnemies.append(self.goTillNearestEnemy([-1, 1], piece.x, piece.y))
        listOfEnemies.append(self.goTillNearestEnemy([-1, -1], piece.x, piece.y))
        
        while None in listOfEnemies:
            listOfEnemies.remove(None)
            
            
        return listOfEnemies
    
    # funkcja sprawdzająca czy nie wyszliśmy poza planszę z koordynatami
    def outOfBoard(self, x, y):
        if x < 1 or x > 8 or y < 1 or y > 8:
            return True
        else:
            return False

        
    # Funkcja zwraca koordynaty wrogiego piona w zadanym kierunku o wektorze "vector" od piona "piece"
    def goTillNearestEnemy(self, vector, x, y):
        
        while(not self.squareIsOccupied( x + vector[0], y + vector[1])):
            x += vector[0]
            y += vector[1]
        
        if self.squareIsOccupiedByEnemy(x + vector[0], y + vector[1]):
            # print("enemy spoted for piece : ", piece.x, piece.y, " on ", x + vector[0], y + vector[1])
            return [x + vector[0], y + vector[1]]
        


    # funkcja sprawdza czy za wrogim pionem jest wolne pole, co umożliwia bicie danego piona
    def checkIfKillPossible(self, piece, enemy):
        vector = [enemy[0] - piece.x, enemy[1] - piece.y]
        
        if vector[0] > 0:
            vector[0] = 1
        else:
            vector[0] = -1
            
        if vector[1] > 0:
            vector[1] = 1
        else:
            vector[1] = -1
            
        direction = vector.copy()
        
        if piece.isQueen():
            while not self.squareIsOccupied(enemy[0] + vector[0], enemy[1] + vector[1] ):
                piece.possibleKillMoves.update({(enemy[0] + vector[0] , enemy[1] + vector[1])  : enemy})
                vector[0] += direction[0]
                vector[1] += direction[1]
        else:
            if not self.squareIsOccupied(enemy[0] + vector[0], enemy[1] + vector[1] ):
                piece.possibleKillMoves.update({(enemy[0] + vector[0] , enemy[1] + vector[1])  : enemy})
            
    # Funkcja sprawdza czy należy piona przetransformować na damkę
    def checkIfQueen(self):
        # W zależności która kolej, tego gracza pionki zostaną sprawdzone
        if self.turn == 1:
            for piece in self.player1pieces:
                if not piece.isQueen():
                    # Jeśli pion osiągnął koniec planszy
                    if piece.y == 8 :
                        # To zmień go na damkę
                        piece.queen = True
        if self.turn == 2:
            for piece in self.player2pieces:
                if not piece.isQueen():
                    # Jeśli pion osiągnął koniec planszy
                    if piece.y == 1 :
                        # To zmień go na damkę
                        piece.queen = True
                        
    # funkcja licząca stan danej planszy dla algorytmu minimax                    
    def evaluate(self):
        score1, score2 = 0, 0
        for piece in self.player1pieces:
            if piece.isQueen():
                score1 += 0.5
            else:
                score1 += 1
                
        for piece in self.player2pieces:
            if piece.isQueen():
                score2 += 0.5
            else:
                score2 += 1
                
        return score1 - score2
    
    # funkcja przemieszcza piona w dane koordynaty
    def movePiece(self, piece, x, y):
        piece.x = x
        piece.y = y



        
                    
                



        