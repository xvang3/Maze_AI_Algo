import pygame
from bfs_solver import bfs_with_visualization_generator
from dfs_solver import dfs_with_visualization_generator
from heuristic_solver import heuristic_with_visualization_generator
from astar_solver import astar_with_visualization_generator
from maze_generator import generate_random_maze_with_solution
from controls import draw_controls, init_controls, handle_slider_event
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, INITIAL_DELAY, SLIDER_MIN, SLIDER_MAX

def handle_slider_event(event, controls, shared_state):
    """Handle slider events to adjust the speed factor dynamically."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if controls["slider_rect"].collidepoint(event.pos):
            controls["slider_dragging"] = True
    elif event.type == pygame.MOUSEBUTTONUP:
        controls["slider_dragging"] = False
    elif event.type == pygame.MOUSEMOTION and controls["slider_dragging"]:
        controls["slider_knob_x"] = max(
            controls["slider_x"],
            min(event.pos[0], controls["slider_x"] + controls["slider_width"])
        )
        slider_fraction = (controls["slider_knob_x"] - controls["slider_x"]) / controls["slider_width"]
        shared_state["speed_factor"] = max(0.1, round(0.1 + slider_fraction * 4.9, 2))

def pre_render_maze(maze, effective_cell_size):
    """Create a surface with the static maze grid pre-rendered."""
    rows, cols = len(maze), len(maze[0])
    surface = pygame.Surface((cols * effective_cell_size, rows * effective_cell_size))

    for row in range(rows):
        for col in range(cols):
            color = (0, 0, 0) if maze[row][col] == 1 else (255, 255, 255)
            pygame.draw.rect(surface, color, (col * effective_cell_size, row * effective_cell_size, effective_cell_size, effective_cell_size))
            pygame.draw.rect(surface, (200, 200, 200), (col * effective_cell_size, row * effective_cell_size, effective_cell_size, effective_cell_size), 1)

    return surface

def new_maze_action(shared_state, states, generators, algorithms, maze, offsets, effective_cell_size):
    """Generate a new maze and reset states and generators."""
    maze[:] = generate_random_maze_with_solution(len(maze), len(maze[0]), wall_density=0.3)
    for idx, (name, generator) in enumerate(algorithms.items()):
        states[name]["maze"] = maze.copy()
        states[name]["current_node"] = None
        states[name]["visited_nodes"].clear()
        states[name]["solution_path"].clear()
        states[name]["cached_grid"] = pre_render_maze(maze, effective_cell_size)
        states[name]["drawn_nodes"].clear()
        generators[name] = generator(
            states[name]["maze"], (0, 0), (len(maze) - 1, len(maze[0]) - 1), effective_cell_size, offsets[idx], states[name]
        )
    shared_state["new_maze_clicked"] = False

def back_action(shared_state):
    """Return to the algorithm selection screen."""
    shared_state["running"] = False
    shared_state["in_selection"] = True

def initialize_algorithms(maze, offsets, effective_cell_size, shared_state):
    """Initialize states and generators for all algorithms."""
    algorithms = {
        "BFS": bfs_with_visualization_generator,
        "DFS": dfs_with_visualization_generator,
        "Heuristic": heuristic_with_visualization_generator,
        "A*": astar_with_visualization_generator,
    }

    states = {}
    generators = {}

    for idx, (name, generator) in enumerate(algorithms.items()):
        state = {
            "paused": False,
            "running": True,
            "started": False,
            "maze": maze.copy(),
            "current_node": None,
            "visited_nodes": set(),
            "solution_path": [],
            "speed": INITIAL_DELAY,  # Reintroduced speed key
            "speed_factor": shared_state["speed_factor"],
            "time_accumulated": 0.0,  # For time-based updates
            "cached_grid": pre_render_maze(maze, effective_cell_size),  # Pre-render maze grid
            "drawn_nodes": set(),  # Cache for dynamically updated nodes
        }
        states[name] = state
        generators[name] = generator(
            state["maze"], (0, 0), (len(maze) - 1, len(maze[0]) - 1), effective_cell_size, offsets[idx], state
        )

    return algorithms, states, generators


def draw_all_mazes(screen, states, offsets, effective_cell_size, font):
    """Draw all mazes and their labels."""
    for idx, (name, state) in enumerate(states.items()):
        maze_offset = offsets[idx]
        label_surface = font.render(name, True, (0, 0, 0))
        label_rect = label_surface.get_rect(center=(maze_offset[0] + len(state["maze"][0]) * effective_cell_size // 2, maze_offset[1] - 15))
        screen.blit(label_surface, label_rect)
        screen.blit(state["cached_grid"], maze_offset)

        for x, y in state["visited_nodes"]:
            pygame.draw.rect(screen, (255, 255, 0), (maze_offset[0] + y * effective_cell_size, maze_offset[1] + x * effective_cell_size, effective_cell_size, effective_cell_size))
        for x, y in state["solution_path"]:
            pygame.draw.rect(screen, (0, 255, 0), (maze_offset[0] + y * effective_cell_size, maze_offset[1] + x * effective_cell_size, effective_cell_size, effective_cell_size))
        for x, y in state["drawn_nodes"]:
            pygame.draw.rect(screen, (0, 0, 255), (maze_offset[0] + y * effective_cell_size, maze_offset[1] + x * effective_cell_size, effective_cell_size, effective_cell_size))

def update_algorithms(states, generators, shared_state, frame_time):
    """Update the algorithms and track dynamically updated nodes."""
    for name, generator in generators.items():
        state = states[name]
        
        # Synchronize speed with shared_state
        state["speed"] = INITIAL_DELAY / shared_state["speed_factor"]  # Dynamic speed adjustment
        
        if state["started"] and not state["paused"]:
            try:
                # Time-based delay
                state["time_accumulated"] += frame_time
                if state["time_accumulated"] >= state["speed"]:
                    action, data = next(generator)
                    if action == "process":
                        state["current_node"] = data
                        state["drawn_nodes"].clear()
                        state["drawn_nodes"].add(data)
                    elif action == "visit":
                        state["visited_nodes"].add(data)
                        state["drawn_nodes"].add(data)
                    elif action == "path":
                        state["solution_path"] = data
                        state["drawn_nodes"].update(data)
                    state["time_accumulated"] -= state["speed"]
            except StopIteration:
                state["started"] = False

        # Synchronize pause and start state with shared controls
        state["paused"] = shared_state["paused"]
        state["started"] = shared_state["started"]

        # Reset on stop
        if shared_state["stop_clicked"]:
            state["current_node"] = None
            state["visited_nodes"].clear()
            state["solution_path"].clear()
            state["drawn_nodes"].clear()


def multi_algo_comparison(screen, font, shared_state):
    """Run a side-by-side comparison of multiple algorithms."""
    rows, cols = 10, 10
    margin = 20
    vertical_padding = 30

    available_width = SCREEN_WIDTH - margin * 5
    effective_cell_size = min(available_width // (cols * 4), CELL_SIZE)
    maze = generate_random_maze_with_solution(rows, cols, wall_density=0.3)
    offsets = [(margin + (effective_cell_size * cols + margin) * i, vertical_padding) for i in range(4)]

    algorithms, states, generators = initialize_algorithms(maze, offsets, effective_cell_size, shared_state)
    controls = init_controls(SCREEN_WIDTH, rows, cols, shared_state, offset_x=20, offset_y=SCREEN_HEIGHT - 150)

    for button in controls["buttons"]:
        if button.text == "New Maze":
            button.action = lambda: new_maze_action(shared_state, states, generators, algorithms, maze, offsets, effective_cell_size)
        elif button.text == "Back":
            button.action = lambda: back_action(shared_state)

    clock = pygame.time.Clock()
    label_font = pygame.font.Font(None, 24)
    running = True

    while running:
        frame_time = clock.get_time()
        screen.fill((255, 255, 255))
        draw_all_mazes(screen, states, offsets, effective_cell_size, font)
        draw_controls(screen, controls, shared_state, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            handle_slider_event(event, controls, shared_state)
            for button in controls["buttons"]:
                button.handle_event(event)

        if shared_state.get("in_selection"):
            running = False

        update_algorithms(states, generators, shared_state, frame_time)

        if shared_state["stop_clicked"]:
            for idx, (name, generator) in enumerate(algorithms.items()):
                states[name]["maze"] = maze.copy()
                generators[name] = generator(
                    states[name]["maze"], (0, 0), (rows - 1, cols - 1), effective_cell_size, offsets[idx], states[name]
                )
            shared_state["stop_clicked"] = False

        pygame.display.flip()
        clock.tick(30)

    return
