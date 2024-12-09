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

    # Initialize state variables for visualization
    state["current_node"] = None
    state["visited_nodes"] = set()
    state["solution_path"] = []

    # Colors for visualization
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    while queue:
        current = queue.popleft()
        state["current_node"] = current  # Track the current node
        yield ("process", current)  # Yield the current node for visualization

        # Dynamic delay
        pygame.time.delay(max(1, int(state["speed"])))  # Use updated speed from the slider
        print(f"Applying delay: {state['speed']} ms for bfs")

        if current == goal:
            # Reconstruct the solution path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            state["solution_path"] = path  # Save the solution path in the state
            yield ("path", path)  # Signal the main loop to visualize the solution
            return

        # Process neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny))
                parent[(nx, ny)] = current
                state["visited_nodes"].add((nx, ny))  # Track visited nodes
                yield ("visit", (nx, ny))  # Signal the main loop to mark as visited

    yield ("no_path", None)
