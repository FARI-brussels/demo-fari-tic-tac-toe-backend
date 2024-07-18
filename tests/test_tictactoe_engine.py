import unittest
from tictactoe_engine import find_best_move

class TestTicTacToeEngine(unittest.TestCase):

    def abcdfind_best_move_empty_board(self):
        board = [[' ' for _ in range(3)] for _ in range(3)]
        move, player, win = find_best_move(board)
        self.assertIn(player, ['X', 'O'])
        self.assertEqual(move, (0, 0))

    def abcdfind_best_move_one_move(self):
        board = [['X', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 2))

    def abcdfind_best_move_one_move2(self):
        board = [['X', ' ', 'O'],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 1))

    def abcdabcdfind_best_move_block_win(self):
        board = [['X', 'X', ' '],
                 ['O', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (0, 2))

    def abcdfind_best_move_block_win2(self):
        board = [[' ', 'O', ' '],
                 [' ', ' ', ' '],
                 [' ', 'X', 'X']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (2, 0))

    def abcdfind_best_move_block_win3(self):
        board = [[' ', 'O', 'X'],
                 [' ', ' ', ' '],
                 [' ', ' ', 'X']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (1, 2))

    def abcdfind_best_move_block_win4(self):
        board = [[' ', 'X', 'O'],
                 [' ', ' ', ' '],
                 [' ', ' ', 'O']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'X')
        self.assertEqual(move, (1, 2))

    def test_find_best_move_win(self):
        board = [['X', 'X', ' '],
                 ['O', 'O', ' '],
                 [' ', 'X', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertTrue(win)
        self.assertEqual(move, (1, 2))

    def test_find_best_move_win2(self):
        board = [['O', 'O', ' '],
                 [' ', 'X', ' '],
                 [' ', 'X', 'X']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'O')
        self.assertEqual(move, (0, 2))
        self.assertTrue(win)

    def test_find_best_move_win3(self):
        board = [['X', 'X', ' '],
                 [' ', 'O', ' '],
                 [' ', 'O', 'O']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'X')
        self.assertEqual(move, (0, 2))
        self.assertTrue(win)
        

    def abcdfind_win(self):
        board = [['X', 'X', 'X'],
                 ['O', 'O', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(player, 'X')
        self.assertEqual(move, None)
        self.assertTrue(win)

    def abcdfind_best_move_already_won(self):
        board = [['X', 'X', 'X'],
                 ['O', ' ', ' '],
                 [' ', ' ', ' ']]
        move, player, win = find_best_move(board)
        self.assertEqual(move, None)
        self.assertTrue(win)


if __name__ == '__main__':
    unittest.main()
    
