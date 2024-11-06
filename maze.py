import random
import matplotlib.pyplot as plt

# Define maze dimensions
width, height = 10, 10  # Adjust size as needed
maze = [[{"visited": False, "walls": [True, True, True, True]} for _ in range(width)] for _ in range(height)]

# Directions (dx, dy) for moving in a 2D grid: right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_within_bounds(x, y):
    """Check if (x, y) is within the maze boundaries."""
    return 0 <= x < height and 0 <= y < width

def remove_wall(x1, y1, x2, y2):
    """Remove the wall between two adjacent cells."""
    if x1 == x2:  # Same row, vertical wall
        if y1 < y2:
            maze[x1][y1]["walls"][1] = False  # Remove right wall
            maze[x2][y2]["walls"][3] = False  # Remove left wall
        else:
            maze[x1][y1]["walls"][3] = False  # Remove left wall
            maze[x2][y2]["walls"][1] = False  # Remove right wall
    elif y1 == y2:  # Same column, horizontal wall
        if x1 < x2:
            maze[x1][y1]["walls"][2] = False  # Remove bottom wall
            maze[x2][y2]["walls"][0] = False  # Remove top wall
        else:
            maze[x1][y1]["walls"][0] = False  # Remove top wall
            maze[x2][y2]["walls"][2] = False  # Remove bottom wall

def generate_maze(x, y):
    """Generate the maze using depth-first search."""
    maze[x][y]["visited"] = True
    random.shuffle(directions)  # Randomize directions for each cell

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_within_bounds(nx, ny) and not maze[nx][ny]["visited"]:
            remove_wall(x, y, nx, ny)
            generate_maze(nx, ny)

# Start maze generation at top-left corner (0,0)
generate_maze(0, 0)

def draw_maze(maze):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect("equal")
    ax.axis("off")

    for x in range(height):
        for y in range(width):
            if maze[x][y]["walls"][0]:  # Top wall
                ax.plot([y, y + 1], [height - x, height - x], color="black")
            if maze[x][y]["walls"][1]:  # Right wall
                ax.plot([y + 1, y + 1], [height - x, height - x - 1], color="black")
            if maze[x][y]["walls"][2]:  # Bottom wall
                ax.plot([y, y + 1], [height - x - 1, height - x - 1], color="black")
            if maze[x][y]["walls"][3]:  # Left wall
                ax.plot([y, y], [height - x, height - x - 1], color="black")

    plt.show()

# Draw the maze
draw_maze(maze)
