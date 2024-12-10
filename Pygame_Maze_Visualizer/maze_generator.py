import numpy as np
import random
from collections import deque

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

    # Add outer wall border
    maze[0, :] = 1  # Top row
    maze[rows - 1, :] = 1  # Bottom row
    maze[:, 0] = 1  # Left column
    maze[:, cols - 1] = 1  # Right column

    maze[0, 0] = 0
    maze[rows-1, cols-1] = 0

    return maze

def ensure_no_double_open_or_walls(maze, rows, cols):
    """Ensures no 2x3 or 3x2 areas are completely open or completely walls."""
    # Checks for 2x3 blocks
    for i in range(rows - 1):
        for j in range(cols - 2):
            # Extract the 2x3 block
            block = maze[i:i+2, j:j+3]
            if np.all(block == 0) or np.all(block == 1):  
                maze[i + random.choice([0, 1]), j + random.choice([0, 1, 2])] = 1 - maze[i + random.choice([0, 1]), j + random.choice([0, 1, 2])]

    # Checks for 3x2 blocks
    for i in range(rows - 2):
        for j in range(cols - 1):
            # Extract the 3x2 block
            block = maze[i:i+3, j:j+2]
            if np.all(block == 0) or np.all(block == 1):  
                maze[i + random.choice([0, 1, 2]), j + random.choice([0, 1])] = 1 - maze[i + random.choice([0, 1, 2]), j + random.choice([0, 1])]

    return maze

def is_connected(maze, start, end, rows, cols):
    """Checks if there's a path between start and end points using BFS."""
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([start])
    visited[start] = True

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            return True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx, ny] and maze[nx, ny] == 0:
                visited[nx, ny] = True
                queue.append((nx, ny))

    return False

def generate_random_maze_with_solution(rows, cols): #removed wall_density=0.3
    """Generates a maze with a guaranteed solution path."""
    while True:
        maze = generate_maze_with_prims(rows, cols)

        # Ensure the start and end positions are open
        maze[0, 0] = 0
        maze[rows-1, cols-1] = 0

        # Creates a guaranteed solution path
        x, y = 0, 0
        while (x, y) != (rows - 1, cols - 1):
            if random.random() > 0.5 and x + 1 < rows:
                x += 1
            elif y + 1 < cols:
                y += 1
            maze[x, y] = 0

        maze = ensure_no_double_open_or_walls(maze, rows, cols)

        if is_connected(maze, (0, 0), (rows - 1, cols - 1), rows, cols):
            break  # Ensures the maze is solvable

    # Debugging: Print the generated maze to the console
    print("Generated Maze (solution guaranteed):")
    for row in maze:
        print(" ".join(map(str, row)))

    return maze

