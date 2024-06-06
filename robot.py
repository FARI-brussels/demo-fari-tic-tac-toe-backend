
import time
import roboticstoolbox as rtb
import numpy as np
import spatialmath as sm
import spatialgeometry as sg
from pydrake.solvers import MathematicalProgram, Solve
# conda install -c conda-forge libstdcxx-ng=12
import swift
from robotsAPI import Lite6API
import json
from vision import image_to_tictactoe_grid
from tictactoe_engine import find_best_move

CONTROL_FREQUENCY = 25

def jacobian_i_k_optimisation(robot, v, qd_max=1):
    # jacobian inverse kinematics with optimisation
    J = robot.jacobe(robot.q)
    prog = MathematicalProgram()
    qd_opt = prog.NewContinuousVariables(6, "v_opt")
    # Define the error term for the cost function
    error = J @ qd_opt - v
    prog.AddCost(error.dot(error))
    # Add bounding box constraint for joint velocities
    lower_bounds = [-qd_max] * 6  # Lower bounds for each joint velocity
    upper_bounds = [qd_max] * 6   # Upper bounds for each joint velocity
    prog.AddBoundingBoxConstraint(lower_bounds, upper_bounds, qd_opt)
    # Solve the optimization problem
    result = Solve(prog)
    return result.is_success(), result.GetSolution(qd_opt)


class OXOPlayer:
    def __init__(self, robot, drawing_board_origin, q_rest=None, control_loop_rate=30, api=None, simulation=None, scene=None, record=False):
        self.robot = robot
        self.api = api
        self.drawing_board_origin = drawing_board_origin
        self.simulation = simulation
        self.scene = scene
        if self.simulation:
            self.simulation.launch(realtime=True)
            self.simulation.add(self.robot)
            for ob in scene:
                self.simulation.add(ob)
        if self.api:
            robot.q = self.api.get_joint_positions(is_radian=True)
        self.record = record
        self.control_loop_rate = control_loop_rate
        self.dt = 1/control_loop_rate
        self.traj = []
        self.previous_grid_state = None
        self.grid_size = None
        self.grid_center = None
        self.q_rest = q_rest

        
    def move_to(self, dest, gain=2, treshold=0.001, qd_max=1): 
        arrived = False
        while not arrived:
            if self.api:
                q = self.api.get_joint_positions(is_radian=True)
                self.robot.q = q
            else:
                q = self.robot.q
            if isinstance(dest, sm.SE3) or (isinstance(dest, np.ndarray) and dest.shape==(4,4)):
                v, arrived = rtb.cp_servo(self.robot.fkine(q), dest, gain=gain, threshold=treshold)
                qd = jacobian_i_k_optimisation(self.robot, v, qd_max=qd_max)[1]
            else:
                qd, arrived = rtb.jp_servo(q, dest, gain=gain, threshold=treshold)
            self.robot.qd = qd
            self.step(qd, control_variable="qd")
        if self.api:
            self.api.set_joint_velocities([0, 0, 0, 0, 0, 0], is_radian=True)
        return arrived, self.robot.q

    def step(self, value, control_variable="qd"):
        if self.api:
            if control_variable == "qd":
                self.api.set_joint_velocities(value, is_radian=True)
            elif control_variable == "q":
                self.api.set_joint_positions(value, is_radian=True)
            if not self.simulation:
                time.sleep(self.dt)
        else: 
            self.simulation.step(self.dt)
        if self.record:
            self.traj.append(self.robot._fk_dict())
            
    
    def draw_grid(self, grid_center, grid_size, lift_height=0.01, qd_max=1):
        grid_center = self.drawing_board_origin*grid_center
        self.grid_size = grid_size
        self.grid_center = grid_center
        
        for i in [-1, 1]:
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * i, -lift_height),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * i, 0), qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * -i, 0), qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * -i, -lift_height), qd_max=qd_max)
        for i in [-1, 1]: 
            self.move_to(grid_center * sm.SE3(grid_size/2 * -i, grid_size/6 * i, -lift_height),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/2 * -i, grid_size/6 * i, 0),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/2 * i, grid_size/6 * i, 0),  qd_max=qd_max)
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest)

    def draw_x(self, center: sm.SE3, length, lift_height=0.01, qd_max=1):
        half_length = length / 2
        self.move_to(center * sm.SE3(-half_length, -half_length, -lift_height), qd_max=qd_max)
        self.move_to(center * sm.SE3(-half_length, -half_length, 0), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, half_length, 0), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, half_length, -lift_height), qd_max=qd_max)
        
        self.move_to(center * sm.SE3(-half_length, half_length, -lift_height), qd_max=qd_max)
        self.move_to(center * sm.SE3(-half_length, half_length, 0), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, -half_length, 0), qd_max=qd_max)
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest)

    def draw_o(self, center: sm.SE3, radius, lift_height=0.01):
        for i in range(50):
            theta = 2 * np.pi * i / 50
            T = center * sm.SE3(radius * np.cos(theta), radius * np.sin(theta), 0)
            self.move_to(T, gain=10) 
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest)

    def play(self, image):
        """
        Play a move in the Tic-Tac-Toe game.

        Args:
            image (np.ndarray): Image data.

        Returns:
            dict: Response containing the grid state, move, game status, and winner.
        """
        # Get the current state of the grid
        grid_state = image_to_tictactoe_grid(image)
        # Check if the board has changed
        if self.previous_grid_state is not None and np.array_equal(grid_state, self.previous_grid_state):
            return {"error": "Please play first, the board has not changed"}

        # Find the best move
        best_move, player_letter, win = find_best_move(grid_state)
        if best_move is None or win:
            return {"grid_state": grid_state, "move": f"letter: {player_letter} in {best_move}", "game_is_finished": True, "winner": player_letter}

        cell_center, size = self.get_cell_center(best_move)

        if player_letter == 'X':
            self.draw_x(cell_center, size / 2)
        else:
            self.draw_o(cell_center, size / 2)

        # Update the previous grid state
        self.previous_grid_state = grid_state

        return {"grid_state": grid_state, "move": f"letter: {player_letter} in {best_move}", "game_is_finished": False, "winner": None}
       

    def get_cell_center(self, cell_index):
        cell_size = self.grid_size / 3
        # Calculate the offset from the top-left corner of the grid to the center
        half_grid_size = self.grid_size / 2
        row, col = cell_index
        x = -half_grid_size + (col + 0.5) * cell_size
        y = -half_grid_size + (row + 0.5) * cell_size
        return self.grid_center*sm.SE3(x,y,0), cell_size


    def save_traj(self, path):
        json.dump(self.traj, open(path, "w"))

    
 

  
