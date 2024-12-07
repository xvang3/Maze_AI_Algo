import pygame
from maze_generator import generate_random_maze_with_solution
from bfs_solver import bfs_with_visualization_generator
from dfs_solver import dfs_with_visualization_generator
from heuristic_solver import heuristic_with_visualization_generator
from astar_solver import astar_with_visualization_generator
from controls import draw_controls, init_controls
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, INITIAL_DELAY

def select_algorithm(screen, font):
    """Display a selection menu for algorithms with a background image and return the selected one."""

    # Load and scale the background image
    background_path = "images/maze1.png"
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    algorithms = ["BFS", "DFS", "Heuristic", "A*"]
    buttons = []
    for i, algo in enumerate(algorithms):
        button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200 + i * 60, 200, 50)
        buttons.append((button, algo))

    # Add Exit button
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200 + len(algorithms) * 60 + 20, 200, 50)

    selected = None
    while selected is None:
        # Draw the background image
        screen.blit(background_image, (0, 0))

        # Draw the title
        title = font.render("Select an Algorithm", True, (0, 0, 0))
        title_shadow = font.render("Select an Algorithm", True, (200, 200, 200))  # Add a shadow effect
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 2, 102))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Draw algorithm buttons
        for button, algo in buttons:
            pygame.draw.rect(screen, (0, 0, 255), button)
            text = font.render(algo, True, (255, 255, 255))
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

        # Draw Exit button
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        exit_text = font.render("Exit", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, algo in buttons:
                    if button.collidepoint(event.pos):
                        selected = algo
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()

    return selected



def main():
    pygame.init()
    font = pygame.font.Font(None, 36)

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Solver")

    while True:  # Restart the loop to re-select algorithm
        # Algorithm selection
        selected_algorithm = select_algorithm(screen, font)

        # Maze setup
        rows, cols = 10, 10
        maze = generate_random_maze_with_solution(rows, cols, wall_density=0.3)
        maze_offset = (10, 10)
        maze_width = int(SCREEN_WIDTH * 0.8)

        # Shared state object
        state = {
            "paused": False,
            "running": True,
            "started": False,
            "repeat": False,
            "algorithm": selected_algorithm,
            "maze": maze,
            "in_selection": False,  # Track if returning to selection
            "solved_path": []
        }

        # Generator setup
        def create_generator():
            state["solved_path"] = []
            
            if state["algorithm"] == "BFS":
                return bfs_with_visualization_generator(state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)
            elif state["algorithm"] == "DFS":
                return dfs_with_visualization_generator(state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)
            elif state["algorithm"] == "Heuristic":
                return heuristic_with_visualization_generator(state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)
            elif state["algorithm"] == "A*":
                return astar_with_visualization_generator(state["maze"], (0, 0), (rows - 1, cols - 1), CELL_SIZE, maze_offset)



        state["create_generator"] = create_generator
        state["algorithm_generator"] = create_generator()

        # Control setup with offsets
        controls, slider_x, slider_y, slider_width, slider_height, knob_x = init_controls(
            maze_width, rows, cols, state, offset_x=50, offset_y=30
        )

        # Main loop
        while state["running"]:
            screen.fill((255, 255, 255))

            # Draw maze
            for row in range(rows):
                for col in range(cols):
                    x, y = maze_offset[0] + col * CELL_SIZE, maze_offset[1] + row * CELL_SIZE
                    color = (0, 0, 0) if state["maze"][row, col] == 1 else (255, 255, 255)
                    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, (200, 200, 200), (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Draw controls
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

            # Run selected algorithm visualization if started
            if state["started"] and not state["paused"]:
                try:
                    action, data = next(state["algorithm_generator"])
                    if action == "process":
                        x, y = data
                        pygame.draw.rect(screen, (0, 0, 255), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    elif action == "visit":
                        x, y = data
                        pygame.draw.rect(screen, (255, 255, 0), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    elif action == "path":
                        for x, y in data:
                            pygame.draw.rect(screen, (0, 255, 0), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        state["solved_path"] = data 
                    elif action == "no_path":
                        print("No solution found.")
                except StopIteration:
                    if state["repeat"]:
                        state["algorithm_generator"] = create_generator()
                    else:
                        state["started"] = False

            if state["solved_path"]:
                for x, y in state["solved_path"]:
                    pygame.draw.rect(screen, (0, 255, 0), (maze_offset[0] + y * CELL_SIZE, maze_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        if state.get("in_selection"):
            continue  # Restart to re-select algorithm
        else:
            break

    pygame.quit()


if __name__ == "__main__":
    main()
