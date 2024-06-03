from ultralytics import YOLO
MODEL = YOLO("weights/best.pt")
CLASS_NAMES = ["O", "X", "grid"]


def bb_to_tictactoe_grid(bounding_boxes_dict):
    """
    Converts bounding box coordinates to a Tic-Tac-Toe grid state.

    Args:
        bounding_boxes_dict (dict): Dictionary containing bounding box coordinates.

    Returns:
        list: 3x3 grid representing the Tic-Tac-Toe board state.
    """
    # Extract the bounding box of the grid
    grid_center_x, grid_center_y, grid_w, grid_h = bounding_boxes_dict['grid'][0]
    cell_w = grid_w / 3
    cell_h = grid_h / 3
    GRID_SIZE = cell_w, cell_h
    # Define the boundaries for the grid cells
    left_boundary = grid_center_x - (1.5 * cell_w)
    top_boundary = grid_center_y - (1.5 * cell_h)

    # Define a function to get the cell position given a point
    def get_cell(position):
        col = int((position[0] - left_boundary) // cell_w)
        row = int((position[1] - top_boundary) // cell_h)
        return row, col

    # Initialize an empty 3x3 grid
    grid_state = [[' ' for _ in range(3)] for _ in range(3)]
    
    # Fill in the 'X' marks
    for position in bounding_boxes_dict.get('X', []):
        row, col = get_cell(position[:2])
        grid_state[row][col] = 'X'
    
    # Fill in the 'O' marks
    for position in bounding_boxes_dict.get('O', []):
        row, col = get_cell(position[:2])
        grid_state[row][col] = 'O'

    return grid_state


def preprocess_bboxes(bboxes, class_names, conf_threshold=0.5):
    """
    Preprocesses bounding boxes to filter by confidence threshold.

    Args:
        bboxes (list): List of bounding boxes.
        class_names (list): List of class names.
        conf_threshold (float): Confidence threshold for filtering.

    Returns:
        dict: Dictionary of filtered bounding boxes by class name.
    """
    result = {class_name: [] for class_name in class_names}
    for box in bboxes:
        conf = box.conf.item()
        if conf > conf_threshold:
            # Extract xywh and class index
            xywh = box.xywh.cpu().numpy()[0].tolist()  # Convert to numpy, get the first row, convert to list
            class_idx = int(box.cls.item())
            # Add to result
            class_name = class_names[class_idx]
            result[class_name].append(xywh)

    return result

def image_to_tictactoe_grid(image):
    """
    Converts an image to a Tic-Tac-Toe grid state.

    Args:
        image (str): Path to the image file.

    Returns:
        list: 3x3 grid representing the Tic-Tac-Toe board state.
    """
    results = MODEL("/home/mrcyme/Documents/FARI/repositories/demo-fari-tic-tac-toe-backend/tests/images/test_image.png", stream=False)
    for r in results:
        bboxes = preprocess_bboxes(r.boxes, CLASS_NAMES)
    return bb_to_tictactoe_grid(bboxes)




#image_to_tictactoe_grid("tictactoegridexample.png")

