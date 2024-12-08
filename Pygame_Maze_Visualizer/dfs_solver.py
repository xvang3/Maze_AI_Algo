import pygame

def dfs_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """DFS generator that yields control after each step for visualization."""
    rows, cols = maze.shape
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}

    # Visualization colors
    blue = (0, 0, 255)  # Current node
    yellow = (255, 255, 0)  # Visited nodes
    green = (0, 255, 0)  # Path nodes

    while stack:
        current = stack.pop()
        x, y = current

        # Yield current node for visualization
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
                stack.append((nx, ny))
                parent[(nx, ny)] = current
                yield ("visit", (nx, ny))  # Yield visited node

    yield ("no_path", None)
