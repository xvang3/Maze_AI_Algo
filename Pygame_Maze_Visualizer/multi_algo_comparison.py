import pygame
from maze_generator import generate_random_maze_with_solution
from bfs_solver import bfs_with_visualization_generator
from dfs_solver import dfs_with_visualization_generator
from heuristic_solver import heuristic_with_visualization_generator
from astar_solver import astar_with_visualization_generator
from controls import draw_controls, init_controls, handle_slider_event
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, INITIAL_DELAY


def multi_algo_comparison(screen, font, shared_state):
    """Run and display all four algorithms side by side with a shared control panel."""
    # Adjust dimensions for horizontal alignment
    rows, cols = 10, 10
    maze_width, maze_height = CELL_SIZE * cols, CELL_SIZE * rows
    margin = 20  # Horizontal spacing between mazes
    vertical_padding = 30  # Padding from the top of the screen
    control_panel_height = 150  # Height of the control panel

    # Calculate effective cell size to fit all four mazes in a row
    available_width = SCREEN_WIDTH - margin * 5  # Account for margins between mazes and edges
    effective_cell_size = min(available_width // (cols * 4), CELL_SIZE)  # Fit four mazes in a row
    maze_width = effective_cell_size * cols

    # Generate a shared maze for all algorithms
    maze = generate_random_maze_with_solution(rows, cols, wall_density=0.3)

    # Positions for each maze
    offsets = [
        (margin + (maze_width + margin) * i, vertical_padding + 30) for i in range(4)  # Add extra padding for labels
    ]

    # Create generators for each algorithm
    algorithms = {
        "BFS": bfs_with_visualization_generator,
        "DFS": dfs_with_visualization_generator,
        "Heuristic": heuristic_with_visualization_generator,
        "A*": astar_with_visualization_generator,
    }
    generators = {}
    states = {}

    for idx, (name, generator) in enumerate(algorithms.items()):
        state = {
            "paused": False,
            "running": True,
            "started": False,
            "maze": maze.copy(),
            "current_node": None,
            "visited_nodes": set(),
            "solution_path": [],
            "speed": INITIAL_DELAY,
            "speed_factor": shared_state["speed_factor"],
        }
        states[name] = state
        generators[name] = generator(
            state["maze"], (0, 0), (rows - 1, cols - 1), effective_cell_size, offsets[idx], state
        )

    # Initialize shared control panel
    controls = init_controls(SCREEN_WIDTH, rows, cols, shared_state, offset_x=20, offset_y=maze_height + vertical_padding + margin + 50)

    clock = pygame.time.Clock()
    running = True

    # Font for algorithm labels
    label_font = pygame.font.Font(None, 24)

    while running:
        screen.fill((255, 255, 255))

        # Draw each maze and its label
        for idx, (name, state) in enumerate(states.items()):
            maze_offset = offsets[idx]

            # Draw the label for the maze
            label_surface = label_font.render(name, True, (0, 0, 0))
            label_rect = label_surface.get_rect(center=(maze_offset[0] + maze_width // 2, maze_offset[1] - 15))
            screen.blit(label_surface, label_rect)

            # Draw the maze
            for row in range(rows):
                for col in range(cols):
                    x = maze_offset[0] + col * effective_cell_size
                    y = maze_offset[1] + row * effective_cell_size
                    color = (0, 0, 0) if state["maze"][row, col] == 1 else (255, 255, 255)
                    pygame.draw.rect(screen, color, (x, y, effective_cell_size, effective_cell_size))
                    pygame.draw.rect(screen, (200, 200, 200), (x, y, effective_cell_size, effective_cell_size), 1)

            # Draw visited nodes
            for x, y in state["visited_nodes"]:
                pygame.draw.rect(screen, (255, 255, 0), (maze_offset[0] + y * effective_cell_size,
                                                         maze_offset[1] + x * effective_cell_size,
                                                         effective_cell_size, effective_cell_size))

            # Draw current node
            if state["current_node"]:
                x, y = state["current_node"]
                pygame.draw.rect(screen, (0, 0, 255), (maze_offset[0] + y * effective_cell_size,
                                                       maze_offset[1] + x * effective_cell_size,
                                                       effective_cell_size, effective_cell_size))

            # Draw solution path
            for x, y in state["solution_path"]:
                pygame.draw.rect(screen, (0, 255, 0), (maze_offset[0] + y * effective_cell_size,
                                                       maze_offset[1] + x * effective_cell_size,
                                                       effective_cell_size, effective_cell_size))

        # Draw control panel
        draw_controls(screen, controls, shared_state, font)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            handle_slider_event(event, controls, shared_state)
            for button in controls["buttons"]:
                button.handle_event(event)

        # Run each algorithm if started and not paused
        for name, generator in generators.items():
            state = states[name]
            if state["started"] and not state["paused"]:
                try:
                    action, data = next(generator)
                    if action == "process":
                        state["current_node"] = data
                    elif action == "visit":
                        state["visited_nodes"].add(data)
                    elif action == "path":
                        state["solution_path"] = data
                except StopIteration:
                    state["started"] = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
