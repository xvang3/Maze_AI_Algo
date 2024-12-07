import numpy as np
import random
import pygame
from collections import deque

def generate_random_maze_with_solution(rows, cols, wall_density=0.3):
    """Generate a random maze with given dimensions, wall density, and a guaranteed solution."""
    # Generate the maze with random walls
    maze = np.random.choice([0, 1], size=(rows, cols), p=[1-wall_density, wall_density])
    
    # Ensure start and goal points are open
    maze[0, 0] = 0
    maze[rows-1, cols-1] = 0

    # Create a guaranteed solution path
    x, y = 0, 0  # Start at the top-left corner
    while (x, y) != (rows - 1, cols - 1):
        # Randomly decide whether to move right or down
        if random.random() > 0.5 and x + 1 < rows:  # Move down if possible
            x += 1
        elif y + 1 < cols:  # Move right if possible
            y += 1
        maze[x, y] = 0  # Clear the path to ensure connectivity

    return maze

def bfs(maze, start, goal):
    """Solve the maze using BFS."""
    rows, cols = maze.shape
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    while queue:
        current = queue.popleft()
        if current == goal:
            # Reconstruct path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]  # Reverse the path to start-to-goal

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny))
                parent[(nx, ny)] = current

    return None  # No path found

def visualize_with_pygame_bfs(maze, cell_size=40, delay=100):
    """Visualize the maze with BFS solution dynamically using Pygame."""
    pygame.init()
    rows, cols = maze.shape
    width, height = cols * cell_size, rows * cell_size

    # Initialize screen and clock
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dynamic BFS Maze Visualization - Pygame")
    clock = pygame.time.Clock()

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    gray = (200, 200, 200)

    # Draw the maze
    for row in range(rows):
        for col in range(cols):
            x, y = col * cell_size, row * cell_size
            color = black if maze[row, col] == 1 else white
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, gray, (x, y, cell_size, cell_size), 1)

    pygame.display.flip()

    # Solve the maze using BFS
    start, goal = (0, 0), (rows - 1, cols - 1)
    solution_path = bfs(maze, start, goal)

    if not solution_path:
        print("No solution found!")
        return

    # Visualize the BFS path step by step
    for x, y in solution_path:
        # Event handling to allow quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Draw the current step
        rect_x, rect_y = y * cell_size, x * cell_size
        pygame.draw.rect(screen, green, (rect_x, rect_y, cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(delay)

    # Keep the window open after completion
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

# Generate a test maze with guaranteed solution
test_maze = generate_random_maze_with_solution(10, 10, wall_density=0.3)

# Visualize the maze with BFS-based path generation
visualize_with_pygame_bfs(test_maze, cell_size=40, delay=100)
