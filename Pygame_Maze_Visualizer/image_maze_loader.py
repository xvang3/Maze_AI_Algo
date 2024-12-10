from PIL import Image
import numpy as np

def process_maze_to_binary(image_path, grid_size):
    """Convert the maze image into a binary matrix of the given grid size."""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_resized = img.resize((grid_size, grid_size), Image.Resampling.LANCZOS)  # Resize to grid size
    matrix = np.array(img_resized)
    threshold = 128  # Adjust threshold for binary conversion
    binary_maze = (matrix < threshold).astype(int)  # Convert to binary: 1 = wall, 0 = path
    return binary_maze


def load_image_maze(image_path, grid_size=21):
    """Load and process a maze from an image file."""
    binary_maze = process_maze_to_binary(image_path, grid_size)
    return binary_maze
