import matplotlib.pyplot as plt
import numpy as np
import time

# Maze dimensions
width, height = 10, 10
maze = np.ones((height, width))  # 1 = wall, 0 = path, -1 = start/goal

# Define start and goal positions
start = (0, 0)
goal = (height - 1, width - 1)
maze[start] = -1  # Mark start
maze[goal] = -1   # Mark goal

# Possible moves: right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initialize visualization
fig, ax = plt.subplots()
im = ax.imshow(maze, cmap="Pastel1")  # Use color map for different cell states
plt.ion()  # Enable interactive mode

def is_within_bounds(x, y):
    """Check if (x, y) is within the maze boundaries."""
    return 0 <= x < height and 0 <= y < width

def visualize_step(x, y, status):
    """Update the visualization at each step."""
    maze[x, y] = status
    im.set_data(maze)
    plt.draw()
    plt.pause(0.1)  # Adjust pause for visualization speed

def dfs(x, y):
    """Simple DFS to solve the maze, visualized step-by-step."""
    if (x, y) == goal:  # Reached goal
        return True
    
    visualize_step(x, y, 0.5)  # Mark as part of the path (visited)

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_within_bounds(nx, ny) and maze[nx, ny] == 1:  # Unvisited path
            if dfs(nx, ny):  # Recursively search next cell
                return True
    
    visualize_step(x, y, 0)  # Mark as backtracked
    return False

# Run DFS from start position
dfs(*start)

# Finalize and display
plt.ioff()  # Turn off interactive mode
plt.show()
