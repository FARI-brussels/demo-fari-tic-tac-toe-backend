# Tic-Tac-Toe Robotic Arm Backend

This project provides a backend for a robotic arm that plays Tic-Tac-Toe. The backend receives commands to draw the grid or to play a move from the frontend, as well as a base64 encoded photo of the current grid when the play order is given.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

//TODO
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server:
    ```sh
    python main.py
    ```

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

## License

This project is licensed under the MIT License.