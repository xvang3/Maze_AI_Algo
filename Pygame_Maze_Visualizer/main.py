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
    maze = generate_random_maze_with_solution(rows, cols, wall_density=0.3)
    maze_offset = (10, 10)
    maze_width = int(SCREEN_WIDTH * 0.8)

    # Control setup
    controls, slider_x, slider_y, slider_width, slider_height, knob_x = init_controls(maze_width, rows, cols)
    speed = INITIAL_DELAY

    # Initialize BFS generator
    bfs_generator = bfs_with_visualization_generator(maze, (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)
    paused = False

    # Main loop
    running = True
    while running:
        screen.fill((255, 255, 255))

        # Draw maze
        for row in range(rows):
            for col in range(cols):
                x, y = maze_offset[0] + col * CELL_SIZE, maze_offset[1] + row * CELL_SIZE
                color = (0, 0, 0) if maze[row, col] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

        # Draw controls
        draw_controls(screen, slider_x, slider_y, slider_width, slider_height, knob_x, controls, speed)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if controls["slider_rect"].collidepoint(event.pos):
                    knob_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                    speed = int((knob_x - slider_x) / slider_width * 1000) + 10
                elif controls["pause_button"].collidepoint(event.pos):
                    paused = not paused
                elif controls["stop_button"].collidepoint(event.pos):
                    maze = generate_random_maze_with_solution(rows, cols, wall_density=0.3)
                    bfs_generator = bfs_with_visualization_generator(maze, (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if controls["slider_rect"].collidepoint(event.pos):
                    knob_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                    speed = int((knob_x - slider_x) / slider_width * 1000) + 10

        # Run BFS generator if not paused
        if not paused:
            try:
                action, data = next(bfs_generator)
                if action == "process":
                    x, y = data
                    pygame.draw.rect(screen, (0, 0, 255), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif action == "visit":
                    x, y = data
                    pygame.draw.rect(screen, (255, 255, 0), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif action == "path":
                    for x, y in data:
                        pygame.draw.rect(screen, (0, 255, 0), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif action == "no_path":
                    print("No solution found.")
            except StopIteration:
                pass  # BFS visualization complete

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
