# Tic-Tac-Toe Robotic Arm Backend

This project provides a backend for a robotic arm that plays Tic-Tac-Toe. The backend receives commands to draw the grid or to play a move from the frontend, as well as a photo of the current grid when the play order is given.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

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
        "grid_state": [[" ", "X", " "], ["O", "X", " "], [" ", " ", " "]],
        "move": "letter : X in (0, 1)",
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

## License

This project is licensed under the MIT License.
