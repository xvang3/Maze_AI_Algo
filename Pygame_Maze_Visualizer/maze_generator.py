import numpy as np
import random

def generate_maze_with_prims(rows, cols):
    """Generates a maze using Prim's algorithm."""
    maze = np.ones((rows, cols), dtype=int)

    start_x, start_y = random.randrange(1, rows, 2), random.randrange(1, cols, 2)
    maze[start_x, start_y] = 0

    walls = []

    def add_neighbors(x, y):
        """Add neighbors to the walls list."""
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows and 0 < ny < cols and maze[nx, ny] == 1:
                walls.append((nx, ny, x, y))

    add_neighbors(start_x, start_y)

    while walls:
        wall = random.choice(walls)
        walls.remove(wall)
        x, y, px, py = wall

        if maze[x, y] == 1:
            if maze[px, py] == 0:
                maze[x, y] = 0
                maze[(x + px) // 2, (y + py) // 2] = 0
                add_neighbors(x, y)

    return maze

def generate_random_maze_with_solution(rows, cols, wall_density=0.3):
    """Adjusts random maze to guarantee solution."""
    #Replace with the Prim's algorithm maze generation
    maze = generate_maze_with_prims(rows, cols)
    
    #Ensure the start and end positions are open and connected
    maze[0, 0] = 0
    maze[rows-1, cols-1] = 0

    #Create guaranteed solution
    x, y = 0, 0
    while (x, y) != (rows - 1, cols - 1):
        if random.random() > 0.5 and x + 1 < rows:
            x += 1
        elif y + 1 < cols:
            y += 1
        maze[x, y] = 0

    return maze
