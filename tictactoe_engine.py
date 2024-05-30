"""
Receive the real world positions of grid, x and o and return the position and letter of the next move
"""
import random
import numpy as np


def evaluate(board):
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
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    
    if x_count > o_count:
        player_letter = 'O'
    elif x_count < o_count:
        player_letter = 'X'
    else:
        player_letter = random.choice(['X', 'O'])

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
    win, winner_letter = check_win(board)
    if win:
        return None, winner_letter
    return best_move, player_letter


def check_win(board):
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

    



