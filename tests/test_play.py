import unittest
import json
import base64
from io import BytesIO
from PIL import Image
from main import app

class TestPlayEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_play(self):
        # Load the test image
        with open('tests/images/test_image.png', 'rb') as image_file:
            image = Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Create the payload
        payload = {
            "image": f"data:image/png;base64,{image_base64}"
        }

        # Send the POST request to the play endpoint
        response = self.app.post('/play', data=json.dumps(payload), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        response_data = json.loads(response.data)
        self.assertIn("grid_state", response_data)
        self.assertIn("move", response_data)
        self.assertIn("game_is_finished", response_data)
        self.assertIn("winner", response_data)

if __name__ == '__main__':
    unittest.main()
