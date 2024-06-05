import unittest
from tictactoe_engine import find_best_move

class TestTicTacToeEngine(unittest.TestCase):

    def test_find_best_move_empty_board(self):
        board = [[' ' for _ in range(3)] for _ in range(3)]
        move, player = find_best_move(board)
        self.assertIn(player, ['X', 'O'])
        self.assertEqual(move, (0, 0))

    def test_find_best_move_one_move(self):
        board = [['X', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (0, 1))

    def test_find_best_move_block_win(self):
        board = [['X', 'X', ' '],
                 ['O', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (0, 2))

    def test_find_best_move_win(self):
        board = [['X', 'X', ' '],
                 ['O', 'O', ' '],
                 [' ', ' ', ' ']]
        move, player = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 2))

if __name__ == '__main__':
    unittest.main()
