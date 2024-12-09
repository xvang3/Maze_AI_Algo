import pygame

# Determine the screen dimensions
def get_screen_dimensions():
    pygame.init()
    info = pygame.display.Info()
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    print(f"Screen dimensions: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")
    return SCREEN_WIDTH, SCREEN_HEIGHT


def calculate_cell_size(screen_width, screen_height, maze_width=10, maze_height=10):
    # Calculate the cell size based on the screen and maze dimensions
    cell_size_width = screen_width // maze_width
    cell_size_height = screen_height // maze_height
    cell_size = min(cell_size_width, cell_size_height)
    print(f"Cell size: {cell_size}")
    return cell_size

# Get the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Cell size for the maze
CELL_SIZE = max(20, min(36, calculate_cell_size(SCREEN_WIDTH, SCREEN_HEIGHT, 10, 10)))

# Initial speed (delay in milliseconds)
INITIAL_DELAY = 0

# Control panel width
CONTROL_PANEL_WIDTH = 200
CONTROL_AREA_WIDTH = 300
CONTROL_MARGIN = 20
