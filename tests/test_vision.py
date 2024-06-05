import unittest
from vision import image_to_tictactoe_grid

class TestVision(unittest.TestCase):

    def test_image_to_tictactoe_grid(self):
        # Path to the test image
        test_image_path = "tests/images/test_image.png"
        
        # Expected grid state
        expected_grid_state = [
            ['X', 'O', ' '],
            [' ', 'X', ' '],
            ['O', ' ', 'X']
        ]
        
        # Get the actual grid state from the function
        actual_grid_state = image_to_tictactoe_grid(test_image_path)
        
        # Assert that the actual grid state matches the expected grid state
        self.assertEqual(actual_grid_state, expected_grid_state)

if __name__ == '__main__':
    unittest.main()
