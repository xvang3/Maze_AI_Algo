import pygame
from collections import deque
from settings import INITIAL_DELAY

def bfs_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """BFS generator that yields control after each step for visualization."""
    rows, cols = maze.shape
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    # Colors for visualization
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    while queue:
        current = queue.popleft()
        x, y = current
        yield ("process", current)  # Yield the current node for visualization

        # Dynamic delay
        # print(f"Speed factor: {state['speed_factor']}")
        state["speed_factor"] = int(INITIAL_DELAY / state["speed_factor"])
        pygame.time.delay(max(1, state["speed"]))  # Ensure non-zero positive delay

        if current == goal:
            # Reconstruct the solution path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            yield ("path", path)  # Signal the main loop to visualize the solution
            return

        # Process neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny))
                parent[(nx, ny)] = current
                yield ("visit", (nx, ny))  # Signal the main loop to mark as visited

    yield ("no_path", None)
