# Tic-Tac-Toe Robotic Arm Backend

This project provides a backend for a robotic arm that plays Tic-Tac-Toe. The backend receives commands to draw the grid or to play a move from the frontend, as well as a base64 encoded photo of the current grid when the play order is given.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```

2. Create a conda enviroment 
    ```sh
    conda create -n tictactoe 
    conda activate tictactoe
    conda install pip
    conda install -c conda-forge libstdcxx-ng=12
    ```
3. Install libraries
    ```sh
    pip install -r requirements.txt
    ```

4. 2. Clone the robotic-toolbox repo and install
    ```sh
    git clone git@github.com:mrcyme/robotics-toolbox-python.git
    cd robotics-toolbox-python
    pip install -e .
    cd rtb-data
    pip install -e .
    ```

## Usage

1. Start the Flask server:
    ```sh
    python main.py --modes Modes --robot_ip ip
    ```
    Command-Line Arguments : 

        --modes: Modes to run the application in. Accepts one or both of SIMULATION and REAL. This argument is required.
        --robot_ip: IP address of the robot for REAL mode. This argument is required if REAL mode is specified.

    Example : 

        1. Simulation Mode only:

        python main.py --modes SIMULATION


        2. Real mode only : 

        python main.py --modes REAL --robot_ip ip


        3. Both Simulation and Real Modes:

        python main.py --modes SIMULATION REAL --robot_ip 192.168.1.159


2. Use the following API endpoints to interact with the backend:

### API Endpoints

#### Draw Grid

- **URL:** `/draw_grid`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "center": [x, y],
        "size": [size_value]
    }
    ```
    x, y are the coordinates of the center of the grid on the screen plan. The plan origin is the bottom left corner of the screen. **x, y and size should be given in meters** 
- **Response:**
    ```json
    {
        "message": "Grid generated successfully"
    }
    ```

##### Draw Grid Example

Here is an example of how to call the `/draw_grid` endpoint:

```sh
curl -X POST http://localhost:5000/draw_grid -H "Content-Type: application/json" -d '{
    "center": [0.15, 0.15],
    "size": [0.1]
}'
```

Response:
```json
{
    "message": "Grid generated successfully"
}
```

#### Play Move

- **URL:** `/play`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
        "image": "base64_encoded_image_data"
    }
    ```
- **Response:**
    ```json
    {
        "grid_state": [["l_00", "l_01", "l_02"], ["l_10", "l_11", "l_12"], ["l_20", "l_21", "l_22"]],
        "move": "letter : l in (i, j)",
        "game_is_finished": Bool,
        "winner": "None if not game_is_finished else l"
    }
    ```
    If the game is finished when the play route is called, it does not write a letter and output the winning letter. If the game will be finished after the drawn letter, it writes a letter and output this letter as winning letter.

##### Play Move Example

Here is an example of how to call the `/play` endpoint with a normal move:

```sh
curl -X POST http://localhost:5000/play -H "Content-Type: application/json" -d '{
    "image": "base64_encoded_image_data"
}'
```

Response:
```json
{
    "grid_state": [["0", "", " "], ["O", "X", " "], ["X", " ", " "]],
    "move": "letter : X in (2,0)",
    "game_is_finished": false,
    "winner": null
}
```

Here is an example of how to call the `/play` endpoint with a winning move:

```sh
curl -X POST http://localhost:5000/play -H "Content-Type: application/json" -d '{
    "image": "base64_encoded_image_data"
}'
```

Response:
```json
{
    "grid_state": [["X", "X", "X"], ["O", "O", " "], ["O", " ", " "]],
    "move": "letter : X in (2, 0)",
    "game_is_finished": true,
    "winner": "X"
}
```

## Code Documentation

### vision.py

- `bb_to_tictactoe_grid(bounding_boxes_dict)`: Converts bounding box coordinates to a Tic-Tac-Toe grid state.
- `preprocess_bboxes(bboxes, class_names, conf_threshold=0.5)`: Preprocesses bounding boxes to filter by confidence threshold.
- `image_to_tictactoe_grid(image)`: Converts an image to a Tic-Tac-Toe grid state.

### main.py

- `draw_grid()`: API endpoint to draw the Tic-Tac-Toe grid.
- `play()`: API endpoint to play a move in the Tic-Tac-Toe game.

### tictactoe_engine.py

- `evaluate(board)`: Evaluates the board to check for a win.
- `minimax(board, depth, is_max, alpha, beta, player_letter)`: Minimax algorithm to find the best move.
- `find_best_move(board)`: Finds the best move for the current board state.
- `check_win(board)`: Checks if there is a win on the board.

## Tests
RUn the tests : 
```sh
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License.
