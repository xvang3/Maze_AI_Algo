import numpy as np
import random

def generate_random_maze_with_solution(rows, cols, wall_density=0.3):
    """Generate a random maze with guaranteed solution."""
    maze = np.random.choice([0, 1], size=(rows, cols), p=[1 - wall_density, wall_density])
    maze[0, 0] = 0
    maze[rows-1, cols-1] = 0

    # Create guaranteed solution
    x, y = 0, 0
    while (x, y) != (rows - 1, cols - 1):
        if random.random() > 0.5 and x + 1 < rows:
            x += 1
        elif y + 1 < cols:
            y += 1
        maze[x, y] = 0

    return maze
