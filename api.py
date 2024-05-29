from flask import Flask, request, jsonify
import base64
import numpy as np
from vision import image_to_tictactoe_grid
from tictactoe_engine import find_best_move
from robot import OXOPlayer
import spatialmath as sm

app = Flask(__name__)

# Initialize the robot and OXOPlayer
robot = ...  # Initialize your robot here
oxoplayer = OXOPlayer(robot)

@app.route('/draw_grid', methods=['POST'])
def draw_grid():
    try:
        data = request.get_json()
        center = data.get('center')
        size = data.get('size')

        if not center or not size:
            return jsonify({"message": "Invalid input"}), 400

        center_position = sm.SE3(center[0], center[1], 0)  # Convert to SE3
        size_value = size[0]  # Assuming size is a single value for simplicity

        oxoplayer.draw_grid(center_position, size_value)
        return jsonify({"message": "Grid generated successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/play', methods=['POST'])
def play():
    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({"message": "Invalid input"}), 400

        # Decode the base64 image
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image = np.frombuffer(image_bytes, dtype=np.uint8)

        # Get the current state of the grid
        grid_state = image_to_tictactoe_grid(image)

        # Find the best move
        best_move, player_letter = find_best_move(grid_state)

        if best_move is None:
            return jsonify({"game_is_finished": True, "winner": player_letter}), 200

        # Draw the move
        row, col = best_move
        cell_center = sm.SE3(row * 10, col * 10, 0)  # Convert to SE3, assuming 10mm per cell

        if player_letter == 'X':
            oxoplayer.draw_x(cell_center, 10)
        else:
            oxoplayer.draw_o(cell_center, 5)

        return jsonify({"game_is_finished": False, "winner": None}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
