import pygame
from heapq import heappush, heappop

def astar_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """A* search generator for visualization."""
    rows, cols = maze.shape
    open_set = []  # Priority queue for A* search
    heappush(open_set, (0, start))  # (f-score, node)
    g_scores = {start: 0}  # Actual cost from start to this node
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
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx, ny] == 0:
                tentative_g_score = g_scores[current] + 1
                if (nx, ny) not in g_scores or tentative_g_score < g_scores[(nx, ny)]:
                    g_scores[(nx, ny)] = tentative_g_score
                    f_score = tentative_g_score + heuristic((nx, ny), goal)
                    parent[(nx, ny)] = current
                    heappush(open_set, (f_score, (nx, ny)))
                    yield ("visit", (nx, ny))  # Yield visited node

    yield ("no_path", None)
