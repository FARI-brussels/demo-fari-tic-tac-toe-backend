from flask import Flask, request, jsonify
import base64
import numpy as np
from vision import image_to_tictactoe_grid
from tictactoe_engine import find_best_move
from robot import OXOPlayer
import spatialmath as sm
import spatialgeometry as sg
import swift
import roboticstoolbox as rtb

app = Flask(__name__)


MODES = ["SIMULATION"]
ROBOT = rtb.models.URDF.Lite6()

api = None
simulation = None
table = sg.Mesh(
        filename=str("/home/mrcyme/Documents/FARI/repositories/demo-fari-robotic-arm/robotic_arm/stand.dae"),
        scale=(1.0,) * 3,
        color=[240, 103, 103],
    )
table.T = table.T * sm.SE3.Tz(0.7)
screen_origin = table.T*sm.SE3.Tx(-0.1)*sm.SE3.Ty(-0.2)*sm.SE3.Tz(0.098)*sm.SE3.RPY([0, 180, 0], order='xyz', unit='deg')

if "SIMULATION" in MODES:
    
    simulation = swift.Swift()
    scene = [table]
    ROBOT.base *=  sm.SE3.Rz(90, 'deg')* sm.SE3.Tz(0.7)

if "REAL" in MODES:
    api=api


q_rest = [100, -9, 50, -170 ,-40,- 190]
q_rest = np.radians(q_rest)
ROBOT.q = q_rest
oxoplayer = OXOPlayer(ROBOT, drawing_board_origin=screen_origin, api=api, simulation=simulation, scene=scene, record=False)


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

        oxoplayer.draw_grid(center_position, size_value, q_rest=q_rest)
        return jsonify({"message": "Grid generated successfully"}), 200

    except Exception as e:
        raise e
        return jsonify({"message": str(e)}), 500

@app.route('/play', methods=['POST'])
def play():
    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({"message": "Invalid input"}), 400

        # Decode the base64 image
        try:
            image_bytes = base64.b64decode(image_data.split(",")[1])
        except IndexError:
            return jsonify({"error": "Invalid image data format"}), 400
        
        image = np.frombuffer(image_bytes, dtype=np.uint8)

        # Get the current state of the grid
        grid_state = image_to_tictactoe_grid(image)

        # Find the best move
        best_move, player_letter = find_best_move(grid_state)

        if best_move is None:
            return jsonify({"grid_state": grid_state, "move" : f"letter : {player_letter} in {best_move}", "game_is_finished": True, "winner": player_letter}), 200
        
        cell_center, size = oxoplayer.get_cell_center(best_move)
        

        if player_letter == 'X':
            oxoplayer.draw_x(cell_center, size/2, q_rest=q_rest)
        else:
            oxoplayer.draw_o(cell_center, size/2, q_rest=q_rest)

        return jsonify({"grid_state": grid_state, "move" : f"letter : {player_letter} in {best_move}", "game_is_finished": True, "winner": player_letter}), 200

    except Exception as e:
        raise e
    
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
