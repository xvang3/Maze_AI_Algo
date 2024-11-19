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


import tkinter as tk

def visualize_with_tkinter(maze, path, cell_size=40):
    root = tk.Tk()
    root.title("Tkinter Visualization")
    rows, cols = maze.shape

    canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            color = "black" if maze[row, col] == 1 else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    for x, y in path:
        x1, y1 = y * cell_size, x * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="gray")

    root.mainloop()

# Test Tkinter Visualization
visualize_with_tkinter(test_maze, test_path)
