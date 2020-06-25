"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    xCount = oCount = 0
    for i in board:
        xCount += i.count(X)
        oCount += i.count(O)
    return O if oCount < xCount else X


def actions(board):
    possibleMoves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possibleMoves.add((i,j))
    return possibleMoves


def result(board, action):
    boardCopy = copy.deepcopy(board)
    i,j = action
    if boardCopy[i][j] is not None:
        raise ValueError('INVALID VALUE')
    boardCopy[i][j] = player(boardCopy)
    return boardCopy


def winner(board):
    validWinner = None
    cases = board + [[i[0] for i in board],[i[1] for i in board],[i[2] for i in board],[board[i][i] for i in range(3)],[board[i][3-1-i] for i in range(3)]]
    if [X,X,X] in cases:
        validWinner = X
    elif [O,O,O] in cases:
        validWinner = O
    return validWinner


def terminal(board):
    if winner(board) in [X,O]:
        return True
    if len(actions(board)) == 0:
        return True
    return False


def utility(board):
    winvar = winner(board)
    return 1 if winvar == X else -1 if winvar == O else 0


def minimax(board):
    if terminal(board):
        return None
    if board == initial_state():
        return (0,1)
    
    current_player = player(board)
    best_value = float("-inf") if current_player == X else float("inf")
    
    for action in actions(board):
        new_value = minimax_value(result(board, action), best_value)
        
        if current_player == X:
            new_value = max(best_value, new_value)
        if current_player == O:
            new_value = min(best_value, new_value)
            
        if new_value != best_value:
            best_value = new_value
            best_action = action

    return best_action

def minimax_value(board, best_value):
    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    value = float("-inf") if current_player == X else float("inf")  
    
    for action in actions(board):
        new_value = minimax_value(result(board, action), value)

        if current_player == X:
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value
