from copy import deepcopy

# realizacja algorytmu minimax
def minimax(board, depth, alpha, beta, maximizingPlayer):
    # jeżeli głębokość równa się zero lub gra została wygrana to zwróć planszę i wartość 
    if depth == 0 or board.gameWon():
        return board.evaluate(), board
    
    
    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for move in getAllMoves(board):
            # liczenie wartości planszy
            evaluation = minimax(move, depth-1, alpha, beta, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            # alfa beta wcięcia
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
                
        return maxEval, best_move
    else:
        
        minEval = float('inf')
        best_move = None
        for move in getAllMoves(board):
            # liczenie wartości planszy
            evaluation = minimax(move, depth-1, alpha, beta, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            # alfa beta wcięcia
            beta = max(beta, minEval)
            if beta <= alpha:
                break
                
        return minEval, best_move
            
            
            
# funkcja symulująca ruch AI
def simulateMove(piece, move, temp_board):
    temp_piece = temp_board.getPiece(piece.x, piece.y)
    temp_piece.move(move[0], move[1])
    temp_board.checkIfQueen()
    
    temp_board.toggleTurn()
    
    return temp_board

# funkcja symulująca bicie AI
def simulateKillMove(piece, pieceToKill, killMove, temp_board):
    temp_piece = temp_board.getPiece(piece.x, piece.y)
    before = temp_piece.isQueen()
    temp_piece.killMove(killMove[0], killMove[1])    
    temp_piece.clearAllMoves()
    temp_board.killPiece(pieceToKill)  
    temp_board.checkIfQueen()
    after = temp_piece.isQueen()
    temp_board.getAllPossibleKills()
    
    if  len(temp_piece.possibleKillMoves) > 0 and not (before == False and after == True ):
        temp_board.killStreak = [True, temp_piece]
        return temp_board
        
    temp_board.killStreak = [False, None]
    temp_board.toggleTurn()
    
    
    return temp_board
            
            
# funkcja wydobywająca wszystkie możliwe stany planszy oraz zwracająca te plansze w liście
def getAllMoves(board):
    moves = []

    if board.turn == 1:
        board.getAllPossibleMoves()
        board.getAllPossibleKills()
        if board.killStreak[0]:
            pieceOnKillingStreak = board.killStreak[1]
            for killMove, pieceToKill in pieceOnKillingStreak.possibleKillMoves.items():
                temp_board = deepcopy(board)
                new_board = simulateKillMove(pieceOnKillingStreak, pieceToKill, killMove, temp_board)
                moves.append(new_board)
        else:
            for piece in board.player1pieces:
                for move in piece.possibleMoves:
                    temp_board = deepcopy(board)
                    new_board = simulateMove(piece, move, temp_board)
                    moves.append(new_board)
                for killMove, pieceToKill in piece.possibleKillMoves.items():
                    temp_board = deepcopy(board)
                    new_board = simulateKillMove(piece, pieceToKill, killMove, temp_board)
                    moves.append(new_board)
                
    
    if board.turn == 2:
        board.getAllPossibleMoves()
        board.getAllPossibleKills()
        if board.killStreak[0]:
            piece = board.killStreak[1]
            for killMove, pieceToKill in piece.possibleKillMoves.items():
                temp_board = deepcopy(board)
                new_board = simulateKillMove(piece, pieceToKill, killMove, temp_board)
                moves.append(new_board)
        else:
            for piece in board.player2pieces:
                for move in piece.possibleMoves:
                    temp_board = deepcopy(board)
                    new_board = simulateMove(piece, move, temp_board)
                    moves.append(new_board)
                for killMove, pieceToKill in piece.possibleKillMoves.items():
                    temp_board = deepcopy(board)
                    new_board = simulateKillMove(piece, pieceToKill, killMove, temp_board)
                    moves.append(new_board)
                
    return moves
                