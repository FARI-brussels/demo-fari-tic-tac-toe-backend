
import time
import roboticstoolbox as rtb
import numpy as np
import spatialmath as sm
import spatialgeometry as sg
from pydrake.solvers import MathematicalProgram, Solve
# conda install -c conda-forge libstdcxx-ng=12
import swift
import json
from vision import image_to_tictactoe_grid
from tictactoe_engine import find_best_move

CONTROL_FREQUENCY = 10

def jacobian_i_k_optimisation(robot, v, z_boundary= 0, qd_max=1, potiential_field=False):
    J = robot.jacobe(robot.q)
    J_trans = J[:3, :]  # Extract the translational part of the Jacobian
    prog = MathematicalProgram()
    qd_opt = prog.NewContinuousVariables(6, "v_opt")

    # Define the error term for the cost function
    error = J @ qd_opt - v
    prog.AddCost(error.dot(error))
    if potiential_field:
        # Calculate the potential field gradient
        robot_position = robot.fkine(robot.q).t  # Get the current end-effector position
        _, gradient = potential_field(robot_position, z_boundary)
        # Incorporate the potential field gradient into the cost function
        prog.AddCost(0.000001*np.dot(gradient, J_trans @ qd_opt))

    # Add bounding box constraint for joint velocities
    lower_bounds = [-qd_max] * 6  # Lower bounds for each joint velocity
    upper_bounds = [qd_max] * 6   # Upper bounds for each joint velocity
    prog.AddBoundingBoxConstraint(lower_bounds, upper_bounds, qd_opt)
    # Solve the optimization problem
    result = Solve(prog)
    return result.is_success(), result.GetSolution(qd_opt)


def potential_field(robot_position, z_limit, influence_distance=0.004):
    potential = 0
    gradient = np.zeros(3)

    z = robot_position[2]
    if z- influence_distance < z_limit :
        # Calculate the potential for z approaching z_limit
        potential += 0.5 * (1.0 / (z_limit - z) - 1.0 / influence_distance)**2
        # Calculate the gradient of the potential
        gradient[2] += (1.0 / (z_limit - z)**3) * (1.0 / (z_limit - z) - 1.0 / influence_distance)
    return potential, gradient

class OXOPlayer:
    def __init__(self, robot, drawing_board_origin, q_rest=None, qd_max = 1, z_boundary = 0, control_loop_rate=25, api=None, simulation=None, scene=None, record=False):
        self.robot = robot
        self.api = api
        self.drawing_board_origin = drawing_board_origin
        self.simulation = simulation
        self.scene = scene
        self.q_rest = q_rest
        self.qd_max = qd_max
        self.record = record
        self.control_loop_rate = control_loop_rate
        self.dt = 1/control_loop_rate
        self.traj = []
        self.previous_grid_state = None
        self.grid_size = None
        self.grid_center = None
        self.z_boundary = z_boundary
        if self.simulation:
            self.simulation.launch(realtime=True)
            self.simulation.add(self.robot)
            for ob in scene:
                self.simulation.add(ob)
        if self.api:
            self.move_to(self.q_rest, qd_max=0.2)
            robot.q = self.api.get_joint_positions(is_radian=True)

        
        
    def move_to(self, dest, gain=2, treshold=0.001, qd_max=0.5): 
        arrived = False
        while not arrived:
            if self.api:
                q = self.api.get_joint_positions(is_radian=True)
                self.robot.q = q
            else:
                q = self.robot.q
            if isinstance(dest, sm.SE3) or (isinstance(dest, np.ndarray) and dest.shape==(4,4)):
                v, arrived = rtb.cp_servo(self.robot.fkine(q), dest, gain=gain, threshold=treshold)
                qd = jacobian_i_k_optimisation(self.robot, v, z_boundary = self.z_boundary, qd_max=qd_max)[1]
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
        else: 
            self.simulation.step(self.dt)
        if self.record:
            self.traj.append(self.robot._fk_dict())

    def calibrate_z_plane(self, grid_center, grid_size, qd_approach=0.1, lift_height=0.01):
        grid_center = self.drawing_board_origin * grid_center
        points = [
            (i, j)
            for i in [-1, 0, 1]
            for j in [-1, 0, 1]
        ]
        for (i, j) in points:
            point = grid_center * sm.SE3(grid_size / 3 * i, grid_size / 3 * j, -lift_height)
            self.move_to(point, qd_max=self.qd_max)
            point = grid_center * sm.SE3(grid_size / 3 * i, grid_size / 3 * j, lift_height)
            print(self.move_to(point, qd_max=qd_approach))
            
    
    def draw_grid(self, grid_center, grid_size, lift_height=0.01, qd_max=1.5):
        grid_center = self.drawing_board_origin*grid_center
        self.grid_size = grid_size
        self.grid_center = grid_center
        
        for i in [-1, 1]:
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * i, -lift_height),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * i, 0), qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * -i, 0), qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/6 * i, grid_size/2 * -i, -lift_height), qd_max=qd_max)
        for i in [-1, 1]: 
            self.move_to(grid_center * sm.SE3(grid_size/2 * -i, grid_size/6 * i, -lift_height)*sm.SE3.Rz(90, unit='deg'),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/2 * -i, grid_size/6 * i, 0)*sm.SE3.Rz(90, unit='deg'),  qd_max=qd_max)
            self.move_to(grid_center * sm.SE3(grid_size/2 * i, grid_size/6 * i, 0)*sm.SE3.Rz(90, unit='deg'),  qd_max=qd_max)
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest, qd_max=0.2)

    def draw_x(self, center: sm.SE3, length, lift_height=0.01, qd_max=1):
        half_length = length / 2
        self.move_to(center * sm.SE3(-half_length, -half_length, -lift_height)*sm.SE3.Rz(-45, unit='deg'), qd_max=qd_max)
        self.move_to(center * sm.SE3(-half_length, -half_length, 0)*sm.SE3.Rz(-45, unit='deg'), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, half_length, 0)*sm.SE3.Rz(-45, unit='deg'), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, half_length, -lift_height), qd_max=qd_max)
        
        self.move_to(center * sm.SE3(-half_length, half_length, -lift_height)*sm.SE3.Rz(45, unit='deg'), qd_max=qd_max)
        self.move_to(center * sm.SE3(-half_length, half_length, 0)*sm.SE3.Rz(45, unit='deg'), qd_max=qd_max)
        self.move_to(center * sm.SE3(half_length, -half_length, 0)*sm.SE3.Rz(45, unit='deg'), qd_max=qd_max)
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest, qd_max=0.2)

    def draw_o(self, center: sm.SE3, radius, lift_height=0.01, qd_max=1):
        self.move_to(center * sm.SE3(radius , 0, -lift_height), qd_max= qd_max)
        for i in range(50):
            theta = 2 * np.pi * i / 50
            T = center * sm.SE3(radius * np.cos(theta), radius * np.sin(theta), 0) #* sm.SE3.Rz(theta, unit='rad')
            self.move_to(T, gain=10) 
        self.move_to(center * sm.SE3(0, radius, -lift_height))
        if self.q_rest.any():
            #probably better to implement qrest
            self.move_to(self.q_rest, qd_max=0.2)

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

        cell_center, size = self.get_cell_center(best_move)
        if best_move:
            if player_letter == 'X':
                self.draw_x(cell_center, size / 2)
            else:
                self.draw_o(cell_center, size / 4)

  

        # Update the previous grid state
        self.previous_grid_state = grid_state
        if win:
            return {"grid_state": grid_state, "move": f"letter: {player_letter} in {best_move}", "game_is_finished": True, "winner": player_letter}
        else:
            return {"grid_state": grid_state, "move": f"letter: {player_letter} in {best_move}", "game_is_finished": False, "winner": None}
       

    def get_cell_center(self, cell_index):
        cell_size = self.grid_size / 3
        # Calculate the offset from the top-left corner of the grid to the center
        half_grid_size = self.grid_size / 2
        row, col = cell_index
        y = -half_grid_size + (col + 0.5) * cell_size
        x = half_grid_size - (row + 0.5) * cell_size
        return self.grid_center*sm.SE3(x,y,0), cell_size


    def save_traj(self, path):
        json.dump(self.traj, open(path, "w"))

    
 

  
