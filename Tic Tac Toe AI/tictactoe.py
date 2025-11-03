import math

X = "X"
O = "O"
EMPTY = None  # Use None as the marker for empty cells


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    i, j = action
    if new_board[i][j] != EMPTY:
        raise ValueError("Invalid move: Cell is not empty.")
    current_player = player(board)
    new_board[i][j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Minimax algorithm that returns the best move for the current player.
    """
    if terminal(board):
        return None

    current = player(board)

    # Helper to find the max value and best move for X
    def max_value(board):
        if terminal(board):
            return utility(board), None
        v = float('-inf')
        best_move = None
        for action in actions(board):
            min_result, _ = min_value(result(board, action))
            if min_result > v:
                v = min_result
                best_move = action
                if v == 1:  # Early exit: best possible outcome
                    break
        return v, best_move

    # Helper to find the min value and best move for O
    def min_value(board):
        if terminal(board):
            return utility(board), None
        v = float('inf')
        best_move = None
        for action in actions(board):
            max_result, _ = max_value(result(board, action))
            if max_result < v:
                v = max_result
                best_move = action
                if v == -1:  # Early exit
                    break
        return v, best_move

    # Call the appropriate helper based on who's playing
    if current == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)
    return move
