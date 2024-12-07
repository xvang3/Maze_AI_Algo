import numpy as np
import random
import tkinter as tk
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

def quit_visualization(event, quit_flag):
    """Set the quit flag to True to stop the visualization."""
    quit_flag[0] = True

def visualize_with_tkinter_bfs(maze, cell_size=40, delay=100):
    """Visualize the maze with BFS solution dynamically."""
    root = tk.Tk()
    root.title("Dynamic BFS Maze Visualization")
    rows, cols = maze.shape

    quit_flag = [False]  # Shared flag to signal quitting

    # Create a frame for the message and canvas
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Add instructions label
    instructions = tk.Label(frame, text="Press 'Q' or 'Esc' to Quit the Visualization", font=("Arial", 12))
    instructions.pack()

    # Add the canvas for the maze
    canvas = tk.Canvas(frame, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    # Bind the 'q' or 'Esc' key to quit the visualization
    root.bind("<q>", lambda event: quit_visualization(event, quit_flag))
    root.bind("<Escape>", lambda event: quit_visualization(event, quit_flag))

    # Draw the maze
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = "black" if maze[row, col] == 1 else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # Solve the maze using BFS
    start, goal = (0, 0), (rows - 1, cols - 1)
    solution_path = bfs(maze, start, goal)

    if not solution_path:
        print("No solution found!")
        return

    # Visualize the BFS path step by step
    for x, y in solution_path:
        if quit_flag[0]:  # Check if quit flag is set
            print("Quitting visualization...")
            break

        x1, y1 = y * cell_size, x * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="gray")
        canvas.update()
        canvas.after(delay)  # Pause to create animation effect

    root.destroy()  # Close the Tkinter window
    root.mainloop()

# Generate a test maze with guaranteed solution
test_maze = generate_random_maze_with_solution(10, 10, wall_density=0.3)

# Visualize the maze with BFS-based path generation
visualize_with_tkinter_bfs(test_maze, cell_size=40, delay=200)
