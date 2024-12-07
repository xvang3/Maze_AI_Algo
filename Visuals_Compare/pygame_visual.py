import numpy as np
import random
import pygame
from collections import deque

def generate_random_maze_with_solution(rows, cols, wall_density=0.3):
    """Generate a random maze with given dimensions, wall density, and a guaranteed solution."""
    maze = np.random.choice([0, 1], size=(rows, cols), p=[1-wall_density, wall_density])
    maze[0, 0] = 0
    maze[rows-1, cols-1] = 0

    # Create a guaranteed solution path
    x, y = 0, 0
    while (x, y) != (rows - 1, cols - 1):
        if random.random() > 0.5 and x + 1 < rows:
            x += 1
        elif y + 1 < cols:
            y += 1
        maze[x, y] = 0

    return maze

def bfs_with_visualization(maze, start, goal, screen, cell_size, delay, maze_offset, controls):
    """Solve the maze using BFS with visualization."""
    rows, cols = maze.shape
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    # Colors
    green = (0, 255, 0)  # Solution path
    blue = (0, 0, 255)  # Processing node
    yellow = (255, 255, 0)  # Visited nodes

    paused = False

    while queue:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if controls["pause_button"].collidepoint(event.pos):
                    paused = not paused
                elif controls["stop_button"].collidepoint(event.pos):
                    return "reset"

        # Handle pause functionality
        if paused:
            continue

        current = queue.popleft()
        x, y = current
        pygame.draw.rect(screen, blue, (maze_offset[0] + y * cell_size, maze_offset[1] + x * cell_size, cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(delay)

        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)

            for x, y in path[::-1]:
                pygame.draw.rect(screen, green, (maze_offset[0] + y * cell_size, maze_offset[1] + x * cell_size, cell_size, cell_size))
                pygame.display.flip()
                pygame.time.delay(delay)
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx, ny] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny))
                parent[(nx, ny)] = current

                pygame.draw.rect(screen, yellow, (maze_offset[0] + ny * cell_size, maze_offset[1] + nx * cell_size, cell_size, cell_size))
                pygame.display.flip()
                pygame.time.delay(delay)

    return None

def draw_controls(screen, slider_x, slider_y, slider_width, slider_height, knob_x, controls, speed):
    """Draw the slider, buttons, and instructions."""
    # Draw slider
    pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, (0, 0, 255), (knob_x, slider_y + slider_height // 2), 10)

    # Draw speed label
    font = pygame.font.Font(None, 24)
    speed_label = font.render(f"Speed: {speed} ms", True, (0, 0, 0))
    screen.blit(speed_label, (slider_x, slider_y - 30))

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    pause_color = (0, 200, 0) if controls["pause_button"].collidepoint(mouse_pos) else (0, 255, 0)
    stop_color = (200, 0, 0) if controls["stop_button"].collidepoint(mouse_pos) else (255, 0, 0)

    pygame.draw.rect(screen, pause_color, controls["pause_button"])
    pygame.draw.rect(screen, stop_color, controls["stop_button"])

    pause_text = font.render("Pause/Resume", True, (255, 255, 255))
    stop_text = font.render("Stop/Reset", True, (255, 255, 255))

    screen.blit(pause_text, (controls["pause_button"].x + 10, controls["pause_button"].y + 10))
    screen.blit(stop_text, (controls["stop_button"].x + 10, controls["stop_button"].y + 10))

    # Draw instructions
    font = pygame.font.Font(None, 18)
    instructions = [
        "Instructions:",
        "- Drag slider to adjust speed.",
        "- Click Pause/Resume to pause/resume visualization.",
        "- Click Stop/Reset to restart from the beginning.",
        "- Press ESC or close the window to quit."
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (slider_x, slider_y + 100 + (i * 20)))

def visualize_with_pygame_bfs(maze, cell_size=40, initial_delay=100):
    """Visualize the maze solving process with controls for speed adjustment, pause, and reset."""
    pygame.init()
    rows, cols = maze.shape

    # Screen dimensions
    screen_width, screen_height = 1280, 720
    maze_width = int(screen_width * 0.8)
    maze_height = int(screen_height * 0.8)
    control_panel_width = screen_width - maze_width
    maze_offset = (10, 10)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BFS Visualization with Enhanced Controls")

    # Slider parameters
    slider_x, slider_y = maze_width + 20, 100
    slider_width, slider_height = 200, 10
    knob_x = slider_x + (slider_width // 2)
    speed = initial_delay

    # Button parameters
    pause_button = pygame.Rect(slider_x, slider_y + 50, 140, 40)
    stop_button = pygame.Rect(slider_x, slider_y + 100, 140, 40)

    controls = {
        "pause_button": pause_button,
        "stop_button": stop_button
    }

    # Draw maze
    def draw_maze():
        for row in range(rows):
            for col in range(cols):
                x, y = maze_offset[0] + col * cell_size, maze_offset[1] + row * cell_size
                color = (0, 0, 0) if maze[row, col] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
                pygame.draw.rect(screen, (200, 200, 200), (x, y, cell_size, cell_size), 1)

    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_maze()

        # Draw control panel
        pygame.draw.rect(screen, (200, 200, 200), (maze_width, 0, control_panel_width, screen_height))
        draw_controls(screen, slider_x, slider_y, slider_width, slider_height, knob_x, controls, speed)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y - 10 <= event.pos[1] <= slider_y + 10:
                    knob_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                    speed = int((knob_x - slider_x) / slider_width * 1000) + 10
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y - 10 <= event.pos[1] <= slider_y + 10:
                    knob_x = max(slider_x, min(event.pos[0], slider_x + slider_width))
                    speed = int((knob_x - slider_x) / slider_width * 1000) + 10

        # Visualize BFS
        result = bfs_with_visualization(maze, (0, 0), (rows - 1, cols - 1), screen, cell_size, speed, maze_offset, controls)
        if result == "reset":
            return visualize_with_pygame_bfs(maze, cell_size, initial_delay)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()

# Generate a test maze and run visualization
test_maze = generate_random_maze_with_solution(10, 10, wall_density=0.3)
visualize_with_pygame_bfs(test_maze, cell_size=40, initial_delay=100)
