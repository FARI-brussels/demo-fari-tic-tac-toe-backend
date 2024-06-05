import requests
import json

# Test the /draw_grid endpoint
def test_draw_grid():
    url = "http://127.0.0.1:5000/draw_grid"
    payload = {
        "center": [0.1, 0.3],
        "size": [0.050, 0.070]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Draw Grid Response:", response.json())

# Test the /play endpoint
def test_play():
    url = "http://127.0.0.1:5000/play"
    
    # Read the base64 encoded image from test.txt
    with open("/home/mrcyme/Documents/FARI/repositories/demo-fari-tic-tac-toe-backend/tests/images/test_image.txt", "r") as file:
        base64_image = file.read().strip()
    
    payload = {
        "image": base64_image
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Play Response:", response.json())

if __name__ == "__main__":
    test_draw_grid()
    test_play()