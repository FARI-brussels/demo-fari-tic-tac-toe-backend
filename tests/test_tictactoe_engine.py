import unittest
from tictactoe_engine import find_best_move

class TestTicTacToeEngine(unittest.TestCase):

    def test_find_best_move_empty_board(self):
        board = [[' ' for _ in range(3)] for _ in range(3)]
        move, player, win = find_best_move(board)
        self.assertIn(player, ['X', 'O'])
        self.assertEqual(move, (0, 0))

    def test_find_best_move_one_move(self):
        board = [['X', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 2))

    def test_find_best_move_one_move2(self):
        board = [['X', ' ', 'O'],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        print(move, player, win)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 1))

    def test_find_best_move_block_win(self):
        board = [['X', 'X', ' '],
                 ['O', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (0, 2))

    def test_find_best_move_win(self):
        board = [['X', 'X', ' '],
                 ['O', 'O', ' '],
                 [' ', 'X', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 2))

    def test_find_win(self):
        board = [['X', 'X', 'X'],
                 ['O', 'O', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'X')
        self.assertEqual(move, None)
        self.assertTrue(win)


if __name__ == '__main__':
    unittest.main()
    def test_find_best_move_already_won(self):
        board = [['X', 'X', 'X'],
                 ['O', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(move, None)
        self.assertTrue(win)
