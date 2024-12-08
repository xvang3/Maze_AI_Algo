import pygame
from maze_generator import generate_random_maze_with_solution
from bfs_solver import bfs_with_visualization_generator
from controls import draw_controls, init_controls
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, INITIAL_DELAY

def main():
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BFS Visualization with Enhanced Controls")

    # Maze setup
    rows, cols = 10, 10
    maze_offset = (10, 10)
    maze_width = int(SCREEN_WIDTH * 0.8)

    # Shared state object
    state = {
        "paused": False,
        "running": True,
        "started": False,
        "repeat": False,
        "speed": INITIAL_DELAY,
        "manual_speed_input": "10",
        "maze": generate_random_maze_with_solution(rows, cols, wall_density=0.3),
        "bfs_generator": None,
    }
    state["bfs_generator"] = bfs_with_visualization_generator(
        state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset
    )

    # Control setup with offsets
    controls = init_controls(maze_width, rows, cols, state, offset_x=50, offset_y=30)

    # Main loop
    while state["running"]:
        screen.fill((255, 255, 255))

        # Draw maze with original size
        for row in range(rows):
            for col in range(cols):
                x, y = maze_offset[0] + col * CELL_SIZE, maze_offset[1] + row * CELL_SIZE
                color = (0, 0, 0) if state["maze"][row, col] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Draw controls
        font = pygame.font.Font(None, 24)
        draw_controls(screen, controls, state, font)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["running"] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state["running"] = False

            # Pass events to each button for handling
            for button in controls["buttons"]:
                button.handle_event(event)

            # Handle slider for speed adjustment
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
                if controls["slider_rect"].collidepoint(event.pos):  # Adjust for slider_rect (fixed key)
                    controls["slider_knob_x"] = max(
                        controls["slider_x"], min(event.pos[0], controls["slider_x"] + controls["slider_width"])
                    )
                    # Map slider position to speed (0-500ms)
                    state["speed"] = int(
                        ((controls["slider_knob_x"] - controls["slider_x"]) / controls["slider_width"]) * 500
                    )

        # Run BFS visualization if started
        if state["started"] and not state["paused"]:
            try:
                action, data = next(state["bfs_generator"])
                if action == "process":
                    x, y = data
                    pygame.draw.rect(
                        screen, (0, 0, 255),
                        (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                elif action == "visit":
                    x, y = data
                    pygame.draw.rect(
                        screen, (255, 255, 0),
                        (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                elif action == "path":
                    for x, y in data:
                        pygame.draw.rect(
                            screen, (0, 255, 0),
                            (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        )
                elif action == "no_path":
                    print("No solution found.")

                # Adjust delay based on speed factor
                delay = int(500 / state["speed_factor"])  # Map speed factor to delay
                pygame.time.delay(delay)
            except StopIteration:
                if state["repeat"]:
                    state["bfs_generator"] = bfs_with_visualization_generator(
                        state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset
                    )
                else:
                    state["started"] = False

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
