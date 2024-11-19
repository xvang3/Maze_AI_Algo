import numpy as np
import random

def generate_random_maze(rows, cols, wall_density=0.3):
    """Generate a random maze with given dimensions and wall density."""
    maze = np.random.choice([0, 1], size=(rows, cols), p=[1-wall_density, wall_density])
    maze[0, 0] = 0  # Ensure starting point is open
    maze[rows-1, cols-1] = 0  # Ensure goal point is open
    return maze

def generate_random_path(maze):
    """Generate a simple random path from top-left to bottom-right."""
    path = [(0, 0)]  # Start at the top-left corner
    x, y = 0, 0
    rows, cols = maze.shape

    while (x, y) != (rows - 1, cols - 1):
        if random.random() > 0.5 and x + 1 < rows:  # Move down
            x += 1
        elif y + 1 < cols:  # Move right
            y += 1
        path.append((x, y))

    return path

# Generate the maze and solution path
test_maze = generate_random_maze(10, 10, wall_density=0.3)  # 10x10 maze with 30% walls
test_path = generate_random_path(test_maze)


import pygame

def visualize_with_pygame(maze, path, cell_size=40):
    pygame.init()
    rows, cols = maze.shape
    screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    pygame.display.set_caption("Pygame Visualization")

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    def draw_grid():
        for row in range(rows):
            for col in range(cols):
                color = BLACK if maze[row, col] == 1 else WHITE
                pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    draw_grid()

    for x, y in path:
        pygame.draw.rect(screen, GREEN, (y * cell_size, x * cell_size, cell_size, cell_size))
        pygame.display.update()
        pygame.time.wait(500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

# Test Pygame Visualization
visualize_with_pygame(test_maze, test_path)
