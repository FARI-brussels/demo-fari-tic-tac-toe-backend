import unittest
import json
import base64
from io import BytesIO
from PIL import Image
from main import initialize_app

class TestPlayEndpoint(unittest.TestCase):

    def setUp(self):
        modes = ["SIMULATION"]  # You can add "REAL" mode if needed and provide the IP address.
        robot_ip = "192.168.1.159"  # Set your robot IP address if testing with REAL mode
        self.app = initialize_app(modes, robot_ip).test_client()
        self.app.testing = True
        
    def test_full_play_player_start(self):
        # Create the payload for drawing the grid
        payload = {
        "center": [0.2, 0.1],
        "size": [0.10, 0.10]
        }

        # Send the POST request to the draw_grid endpoint
        response = self.app.post('/draw_grid', data=json.dumps(payload), content_type='application/json')

        # Check the response status code for drawing the grid
        self.assertEqual(response.status_code, 200)

        # Load the test image for the first move
        with open('tests/images/first_move_player_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            first_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Load the test image for the first move
        with open('tests/images/second_move_player_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            second_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Load the test image for the first move
        with open('tests/images/third_move_player_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            third_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        with open('tests/images/fourth_move_player_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            fourth_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        

        # Create the payload for the first move
        first_move = {
            "image": f"data:image/png;base64,{first_move_base64}"
        }
        # Create the payload for the first move
        second_move = {
            "image": f"data:image/png;base64,{second_move_base64}"
        }
        third_move = {
            "image": f"data:image/png;base64,{third_move_base64}"
        }
        fourth_move = {
            "image": f"data:image/png;base64,{fourth_move_base64}"
        }

        # Send the POST request to the play endpoint for the first move
        response = self.app.post('/play', data=json.dumps(first_move), content_type='application/json')

        # Check the response status code for the first move
        self.assertEqual(response.status_code, 200)

        # Check the response data for the first move
        response_data = json.loads(response.data)
        self.assertEqual([[' ', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], response_data["grid_state"])
        self.assertEqual('letter: X in (0, 0)', response_data["move"])
        self.assertEqual(False, response_data["game_is_finished"])
        self.assertEqual(None, response_data["winner"])
        
        # Check if throw error when the board has not changed
        response = self.app.post('/play', data=json.dumps(first_move), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/play', data=json.dumps(second_move), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual([['X', 'O', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], response_data["grid_state"])
        self.assertEqual('letter: X in (2, 1)', response_data["move"])
        self.assertEqual(False, response_data["game_is_finished"])
        self.assertEqual(None, response_data["winner"])

        response = self.app.post('/play', data=json.dumps(third_move), content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual([['X', 'O', 'O'], [' ', 'O', ' '], [' ', 'X', ' ']], response_data["grid_state"])
        self.assertEqual('letter: X in (2, 0)', response_data["move"])
        self.assertEqual(False, response_data["game_is_finished"])
        self.assertEqual(None, response_data["winner"])

        response = self.app.post('/play', data=json.dumps(fourth_move), content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual([['X', 'O', 'O'], [' ', 'O', ' '], ['X', 'X', 'O']], response_data["grid_state"])
        self.assertEqual('letter: X in (1, 0)', response_data["move"])
        self.assertEqual(True, response_data["game_is_finished"])
        self.assertEqual('X', response_data["winner"])


    def test_full_play_robot_start(self):
        # Create the payload for drawing the grid
        payload = {
        "center": [0.2, 0.1],
        "size": [0.10, 0.10]
        }

        # Send the POST request to the draw_grid endpoint
        response = self.app.post('/draw_grid', data=json.dumps(payload), content_type='application/json')

        # Check the response status code for drawing the grid
        self.assertEqual(response.status_code, 200)

        # Load the test image for the first move
        with open('tests/images/first_move_robot_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            first_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Load the test image for the first move
        with open('tests/images/second_move_robot_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            second_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Load the test image for the first move
        with open('tests/images/third_move_robot_start.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            third_move_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Create the payload for the first move
        first_move = {
            "image": f"data:image/png;base64,{first_move_base64}"
        }
        
        # Create the payload for the first move
        second_move = {
            "image": f"data:image/png;base64,{second_move_base64}"
        }
        
        third_move = {
            "image": f"data:image/png;base64,{third_move_base64}"
        }


        # Send the POST request to the play endpoint for the first move
        response = self.app.post('/play', data=json.dumps(first_move), content_type='application/json')
       
        # Check the response status code for the first move
        self.assertEqual(response.status_code, 200)

        # Check the response data for the first move
        response_data = json.loads(response.data)

        self.assertEqual([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], response_data["grid_state"])
        self.assertEqual('letter: O in (0, 0)', response_data["move"])
        self.assertEqual(False, response_data["game_is_finished"])
        self.assertEqual(None, response_data["winner"])


        response = self.app.post('/play', data=json.dumps(second_move), content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual([['O', ' ', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']], response_data["grid_state"])
        self.assertEqual('letter: O in (1, 0)', response_data["move"])
        self.assertEqual(False, response_data["game_is_finished"])
        self.assertEqual(None, response_data["winner"])
        

        response = self.app.post('/play', data=json.dumps(third_move), content_type='application/json')
        response_data = json.loads(response.data)
        self.assertEqual([['O', ' ', 'X'], ['O', 'X', ' '], [' ', ' ', ' ']], response_data["grid_state"])
        self.assertEqual('letter: O in (2, 0)', response_data["move"])
        self.assertEqual(True, response_data["game_is_finished"])
        self.assertEqual("O", response_data["winner"])




if __name__ == "__main__":
    unittest.main()
