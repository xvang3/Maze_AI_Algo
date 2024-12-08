import pygame
from heapq import heappush, heappop

def heuristic_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """Heuristic search generator for visualization."""
    rows, cols = maze.shape
    open_set = []  # Priority queue for heuristic search
    heappush(open_set, (0, start))  # (heuristic value, node)
    visited = set()
    visited.add(start)
    parent = {}

    # Heuristic function: Manhattan distance
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    while open_set:
        _, current = heappop(open_set)
        x, y = current

        # Yield the current node for visualization
        yield ("process", current)

        # Dynamic delay
        pygame.time.delay(state["speed"])

        if current == goal:
            # Reconstruct and visualize the path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            yield ("path", path[::-1])  # Reverse path for start-to-goal
            return

        # Process neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                h_value = heuristic((nx, ny), goal)
                heappush(open_set, (h_value, (nx, ny)))
                yield ("visit", (nx, ny))  # Yield visited node

    yield ("no_path", None)
