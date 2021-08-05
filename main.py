import pygame, sys
from constants import *
from board import *
from minimax.algorithm import minimax


# inicjalizacja modułu pygame
pygame.init()

# inicjalizacja powierzchnii do rysowania
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# funkcja zwraca koordynaty pól na planszy na podstawie kliknięcia myszy
def getSquareAtPixel(mouseX, mouseY):
        squareX = mouseX // SIZE + 1
        squareY = mouseY // SIZE + 1
        
        return squareX, squareY

# funkcja rysująca wszystkie zmiany na planszy
def drawAllMovements(piece):
    board.drawBoard(WIN, piece)
    
    pygame.display.update()



def main():
    
    global board, mouseClicked
    
    mousex = 0 # służy do przechowywania współrzędnej x kliknięcia myszy
    mousey = 0 # służy do przechowywania współrzędnej y kliknięcia myszy
    
    killStreak = False  # 
    
    
    piece = None
    
    # inicjalizacja planszy
    board = Board(COLOR1P, COLOR2P, COLOR1SQ, COLOR2SQ)
    board.initializePieces()
    
    
    # pętla główna programu
    while True:
        # przechowywanie kliknięcia myszy
        mouseClicked = False
        
        
        # wydobycie wszystkich eventów z gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP: # mysz została wciąnięta
                mousex, mousey = event.pos
                mouseClicked = True
        
        # AI wykonuje ruch
        if board.turn == 1:
            value, new_board = minimax(board, 4, float('-inf'), float('inf'), True)
            board = new_board

        # mysz została wciśnięta
        if mouseClicked :
            
            # gdy żaden pion nie jest wybrany
            if piece == None:
                board.getAllPossibleMoves()   
                board.getAllPossibleKills()
                squarex, squarey = getSquareAtPixel(mousex, mousey)
                piece = board.getPiece(squarex, squarey)
                if board.gameWon():
                    print("The game has been ended")
                    pygame.time.delay(2000)
                    pygame.quit()
                    sys.exit() 
            else:    
                if killStreak:
                    piece.clearAllMoves()
                    board.getAllPossibleKills()
                squarex, squarey = getSquareAtPixel(mousex, mousey)
                # obsługa ruchu
                if piece.checkIfMoveIsPossible(squarex, squarey) and not killStreak:
                    piece.move(squarex, squarey)
                    if board.gameWon():
                        print("The game has been ended")
                        pygame.time.delay(2000)
                        pygame.quit()
                        sys.exit() 
                    board.checkIfQueen()
                    piece = None
                    board.toggleTurn()
                    
                # obsługa zbijania
                elif piece.checkIfKillIsPossible(squarex, squarey) :
                    if board.gameWon():
                        drawAllMovements(piece)
                        print("The game has been ended")
                        pygame.time.delay(2000)
                        pygame.quit()
                        sys.exit() 
                    board.killPiece(piece.possibleKillMoves[squarex, squarey])
                    before = piece.isQueen()
                    piece.move(squarex, squarey)
                    board.checkIfQueen()
                    after = piece.isQueen()
                    piece.clearAllMoves()
                    board.getAllPossibleKills()
                    if len(piece.possibleKillMoves) > 0 and not (before == False and after == True ):
                        killStreak = True
                    else:
                        piece = None
                        
                        board.toggleTurn()
                        killStreak = False

                else:
                    if not killStreak:
                        piece = board.getPiece(squarex, squarey)
        
        # rysowanie zmian na planszy
        drawAllMovements(piece)    
            
            
            
            
        
if __name__ == '__main__':
    main()