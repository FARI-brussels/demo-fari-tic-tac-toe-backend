# main.py

import argparse
from flask import Flask, request, jsonify
import base64
import numpy as np
from vision import image_to_tictactoe_grid
from tictactoe_engine import find_best_move
from robot import OXOPlayer
import spatialmath as sm
import spatialgeometry as sg
from PIL import Image
import io
import swift
import roboticstoolbox as rtb
import cv2
import os
from robotsAPI import Lite6API

app = Flask(__name__)

def initialize_app(modes, robot_ip=None):
    global ROBOT, api, simulation, scene, oxoplayer

    # Validate modes
    MODES = modes
    if not MODES:
        raise ValueError("At least one mode must be specified: SIMULATION or REAL.")

    ROBOT = rtb.models.URDF.Lite6()
    ROBOT_IP = robot_ip if robot_ip else "192.168.1.159"
    ROBOT.base *= sm.SE3.Rz(180, 'deg') * sm.SE3.Tz(0.7)

    api = None
    simulation = None
    scene = []

    table = sg.Mesh(
        filename=str(os.path.abspath("assets/stand.dae")),
        scale=(1.0,) * 3,
        color=[240, 103, 103],
    )
    table.T = table.T * sm.SE3.Rz(90, 'deg')* sm.SE3.Tz(0.7) 
    screen_origin = table.T * sm.SE3.Tx(-0.1) * sm.SE3.Ty(-0.2) * sm.SE3.Tz(0.1) * sm.SE3.RPY([0, 180, 0], order='xyz', unit='deg')

    if "SIMULATION" in MODES:
        simulation = swift.Swift()
        scene.append(table)

    if "REAL" in MODES:
        if not ROBOT_IP:
            raise ValueError("Robot IP must be provided for REAL mode.")
        api = Lite6API(ip=ROBOT_IP)

    q_rest = [100, -9, 50, -170, -40, -190]
    q_rest = np.radians(q_rest)
    ROBOT.q = q_rest
    oxoplayer = OXOPlayer(ROBOT, drawing_board_origin=screen_origin, q_rest=q_rest, api=api, simulation=simulation, scene=scene, record=False)
    return app

@app.route('/draw_grid', methods=['POST'])
def draw_grid():
    """
    API endpoint to draw the Tic-Tac-Toe grid.

    Request Body:
        center (list): Coordinates of the grid center.
        size (list): Size of the grid.

    Returns:
        json: Response message.
    """
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
        raise e
        return jsonify({"message": str(e)}), 500

@app.route('/play', methods=['POST'])
def play():
    """
    API endpoint to play a move in the Tic-Tac-Toe game.

    Request Body:
        image (str): Base64 encoded image data.

    Returns:
        json: Response containing the grid state, move, game status, and winner.
    """
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

        # Convert the decoded bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        # Convert the PIL Image to a numpy array
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Use the play method of OXOPlayer
        response = oxoplayer.play(image)

        if "error" in response:
            return jsonify({"message": response["error"]}), 400

        return jsonify(response), 200

    except Exception as e:
        raise e
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Tic-Tac-Toe Flask app.")
    parser.add_argument('--modes', type=str, nargs='+', required=True, choices=["SIMULATION", "REAL"], help="Modes to run the application in.")
    parser.add_argument('--robot_ip', type=str, help="IP address of the robot for REAL mode.")
    args = parser.parse_args()

    initialize_app(args.modes, args.robot_ip).run(debug=True)
