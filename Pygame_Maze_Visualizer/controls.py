import pygame

def init_controls(maze_width, rows, cols):
    """Initialize UI control components."""
    slider_x, slider_y = maze_width + 20, 150
    slider_width, slider_height = 200, 10
    knob_x = slider_x + (slider_width // 2)

    pause_button = pygame.Rect(slider_x, slider_y + 50, 140, 40)
    stop_button = pygame.Rect(slider_x, slider_y + 100, 140, 40)
    new_maze_button = pygame.Rect(slider_x, slider_y + 150, 140, 40)
    reset_speed_button = pygame.Rect(slider_x, slider_y + 200, 140, 40)
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)

    controls = {
        "pause_button": pause_button,
        "stop_button": stop_button,
        "new_maze_button": new_maze_button,
        "reset_speed_button": reset_speed_button,
        "slider_rect": slider_rect,
        "paused": False
    }

    return controls, slider_x, slider_y, slider_width, slider_height, knob_x

def draw_controls(screen, slider_x, slider_y, slider_width, slider_height, knob_x, controls, speed):
    """Draw the slider, buttons, instructions, and algorithm label."""
    font = pygame.font.Font(None, 24)

    # Draw slider
    pygame.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, (0, 0, 255), (knob_x, slider_y + slider_height // 2), 10)

    # Draw speed label
    speed_label = font.render(f"Speed: {speed} ms", True, (0, 0, 0))
    screen.blit(speed_label, (slider_x, slider_y - 30))

    # Draw buttons
    pygame.draw.rect(screen, (0, 255, 0), controls["pause_button"])
    pygame.draw.rect(screen, (255, 0, 0), controls["stop_button"])
    pygame.draw.rect(screen, (0, 0, 255), controls["new_maze_button"])
    pygame.draw.rect(screen, (255, 255, 0), controls["reset_speed_button"])

    pause_text = font.render("Pause/Resume", True, (255, 255, 255))
    stop_text = font.render("Stop", True, (255, 255, 255))
    new_maze_text = font.render("New Maze", True, (255, 255, 255))
    reset_speed_text = font.render("Reset Speed", True, (0, 0, 0))

    screen.blit(pause_text, (controls["pause_button"].x + 10, controls["pause_button"].y + 10))
    screen.blit(stop_text, (controls["stop_button"].x + 35, controls["stop_button"].y + 10))
    screen.blit(new_maze_text, (controls["new_maze_button"].x + 20, controls["new_maze_button"].y + 10))
    screen.blit(reset_speed_text, (controls["reset_speed_button"].x + 10, controls["reset_speed_button"].y + 10))

    # Draw instructions
    instructions = [
        "Instructions:",
        "- Adjust speed with the slider.",
        "- Pause or resume with the Pause/Resume button.",
        "- Stop restarts the current maze.",
        "- New Maze generates a new maze.",
        "- Reset Speed resets to default speed.",
        "- Press ESC or close the window to quit."
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (slider_x, slider_y + 250 + (i * 20)))

    # Algorithm label
    algorithm_label = font.render("Algorithm: BFS", True, (0, 0, 0))
    screen.blit(algorithm_label, (slider_x, 20))
