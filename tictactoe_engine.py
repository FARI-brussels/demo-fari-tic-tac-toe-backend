"""
Receive the real world positions of grid, x and o and return the position and letter of the next move
"""
import random
import numpy as np


def evaluate(board):
    """
    Evaluates the board to check for a win.

    Args:
        board (list): 3x3 grid representing the Tic-Tac-Toe board state.

    Returns:
        int: Score indicating the result of the evaluation.
    """
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return 10 if board[i][0] == 'X' else -10
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return 10 if board[0][i] == 'X' else -10

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return 10 if board[0][0] == 'X' else -10

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return 10 if board[0][2] == 'X' else -10

    return 0

def minimax(board, depth, is_max, alpha, beta, player_letter):
    """
    Minimax algorithm to find the best move.

    Args:
        board (list): 3x3 grid representing the Tic-Tac-Toe board state.
        depth (int): Current depth of the recursion.
        is_max (bool): Flag indicating if the current move is maximizing.
        alpha (float): Alpha value for alpha-beta pruning.
        beta (float): Beta value for alpha-beta pruning.
        player_letter (str): Letter representing the current player ('X' or 'O').

    Returns:
        int: Best score for the current move.
    """
    score = evaluate(board)

    if score == 10:
        return score - depth

    if score == -10:
        return score + depth

    if not any(' ' in row for row in board):
        return 0

    if is_max:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X' if player_letter == 'X' else 'O'
                    value = minimax(board, depth+1, not is_max, alpha, beta, player_letter)
                    max_eval = max(max_eval, value)
                    alpha = max(alpha, value)
                    board[i][j] = ' '
                    if beta <= alpha:
                        break
        return max_eval

    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O' if player_letter == 'X' else 'X'
                    value = minimax(board, depth+1, not is_max, alpha, beta, player_letter)
                    min_eval = min(min_eval, value)
                    beta = min(beta, value)
                    board[i][j] = ' '
                    if beta <= alpha:
                        break
        return min_eval

def find_best_move(board):
    """
    Finds the best move for the current board state.

    Args:
        board (list): 3x3 grid representing the Tic-Tac-Toe board state.

    Returns:
        tuple: Best move coordinates, the player letter, and a win flag.
    """
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    
    if x_count > o_count:
        player_letter = 'O'
    elif x_count < o_count:
        player_letter = 'X'
    else:
        player_letter = 'O'

    win, winner_letter = check_win(board)
    if win:
        return None, winner_letter, True

    best_move = (-1, -1)
    best_val = float('-inf') if player_letter == 'X' else float('inf')
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player_letter
                move_val = minimax(board, 0, player_letter == 'O', float('-inf'), float('inf'), player_letter)
                board[i][j] = ' '

                if player_letter == 'X' and move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

                if player_letter == 'O' and move_val < best_val:
                    best_move = (i, j)
                    best_val = move_val

    board[best_move[0]][best_move[1]] = player_letter
    win, _ = check_win(board)
    board[best_move[0]][best_move[1]] = ' '

    return best_move, player_letter, win


def check_win(board):
    """
    Checks if there is a win on the board.

    Args:
        board (list): 3x3 grid representing the Tic-Tac-Toe board state.

    Returns:
        tuple: Boolean indicating if there is a win and the winning player letter.
    """
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return True, board[i][0]

        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return True, board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return True, board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return True, board[0][2]

    return False, None

    



