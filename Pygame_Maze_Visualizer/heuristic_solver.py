import pygame
from heapq import heappush, heappop

def heuristic_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """Heuristic search generator for visualization."""
    rows, cols = maze.shape
    open_set = []
    heappush(open_set, (0, start))
    visited = set()
    visited.add(start)
    parent = {}

    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    while open_set:
        _, current = heappop(open_set)
        x, y = current
        yield ("process", current)

        # Dynamic delay
        pygame.time.delay(max(1, int(state["speed"])))

        if current == goal:
            # Reconstruct and visualize the path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            yield ("path", path[::-1])
            return

        # Process neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                heappush(open_set, (heuristic((nx, ny), goal), (nx, ny)))
                yield ("visit", (nx, ny))

    yield ("no_path", None)
