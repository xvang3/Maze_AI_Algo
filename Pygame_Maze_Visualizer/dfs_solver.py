import pygame

def dfs_with_visualization_generator(maze, start, goal, cell_size, maze_offset, state):
    """DFS generator that yields control after each step for visualization."""
    rows, cols = maze.shape
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}

    while stack:
        current = stack.pop()
        x, y = current
        yield ("process", current)

        # Dynamic delay
        pygame.time.delay(max(1, int(state["speed"])))
        # print(f"Applying delay: {state['speed']} ms for dfs")

        if current == goal:
            # Reconstruct and visualize the path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            yield ("path", path[::-1])
            state["solution_path"] = path[::-1]  # Save the solution path
            return

        # Process neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                stack.append((nx, ny))
                yield ("visit", (nx, ny))

    yield ("no_path", None)
