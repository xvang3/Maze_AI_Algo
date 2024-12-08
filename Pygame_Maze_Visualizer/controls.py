from button import Button
import pygame
from maze_generator import generate_random_maze_with_solution
from settings import *

# Constant for number of buttons
NUM_BUTTONS = 6
OTHER_SETTINGS = 2
TOTAL_BUTTONS = NUM_BUTTONS + OTHER_SETTINGS

def init_controls(maze_width, rows, cols, state, offset_x=0, offset_y=0):
    """Initialize UI control components with proper alignment."""
    slider_x = 20  # Shift left
    slider_y = SCREEN_HEIGHT - (40 * TOTAL_BUTTONS)  # Shift up

    # Define button actions
    def start_action():
        state["started"] = True
        if "create_generator" in state:
            state["algorithm_generator"] = state["create_generator"]()  # Create a fresh generator

    def pause_action():
        state["paused"] = not state["paused"]

    def stop_action():
        state["started"] = False

    def new_maze_action():
        state["maze"] = generate_random_maze_with_solution(rows, cols, wall_density=0.3)
        state["started"] = False
        if "create_generator" in state:
            state["algorithm_generator"] = state["create_generator"]()  # Create a fresh generator

    def reset_speed_action():
        state["speed_factor"] = 1.0  # Reset to 1x speed
        controls["slider_knob_x"] = controls["slider_x"]  # Reset slider knob visually
        state["speed"] = int(INITIAL_DELAY / state["speed_factor"])  # Reset the speed factor

    def back_action():
        state["in_selection"] = True  # Set flag to re-enter algorithm selection
        state["running"] = False  # Break the main loop to return

    # Create buttons with actions
    button_width, button_height = 120, 20  # Adjusted button size
    button_spacing = 40  # Adjusted spacing between buttons
    buttons = [
        Button(slider_x, slider_y, button_width, button_height, "Start", (0, 255, 0), (255, 255, 255), start_action),
        Button(slider_x, slider_y + button_spacing, button_width, button_height, "Pause/Resume", (0, 255, 0), (255, 255, 255), pause_action),
        Button(slider_x, slider_y + button_spacing * 2, button_width, button_height, "Stop", (255, 0, 0), (255, 255, 255), stop_action),
        Button(slider_x, slider_y + button_spacing * 3, button_width, button_height, "New Maze", (0, 0, 255), (255, 255, 255), new_maze_action),
        Button(slider_x, slider_y + button_spacing * 4, button_width, button_height, "Reset Speed", (255, 255, 0), (0, 0, 0), reset_speed_action),
        Button(slider_x, slider_y + button_spacing * 5, button_width, button_height, "Back", (255, 165, 0), (255, 255, 255), back_action),  # Add Back button
    ]

    slider_rect = pygame.Rect(slider_x, slider_y + button_spacing * 6, 400, 20)

    controls = {
        "buttons": buttons,
        "slider_rect": slider_rect,
        "slider_knob_x": slider_x,  # Initialize with slider_x first
        "slider_x": slider_x,
        "slider_width": 400,  # Adjusted slider width for better control
    }

    # Now calculate knob_x based on speed_factor
    controls["slider_knob_x"] = slider_x + int(controls["slider_width"] * ((state["speed_factor"] - 1) / 49))

    return controls, slider_x, slider_y, 200, 10, controls["slider_knob_x"]


def draw_controls(screen, controls, state, font):
    """Draw controls with instructions positioned next to their respective buttons."""
    button_instructions = {
        "Start": "Begin the visualization.",
        "Pause/Resume": "Pause or resume the visualization.",
        "Stop": "Reset the current maze.",
        "New Maze": "Generate a new random maze.",
        "Reset Speed": "Reset to 1x speed.",
        "Back": "Return to algorithm selection.",  # Add instruction for Back button
    }

    # Draw buttons and instructions
    for button in controls["buttons"]:
        button.draw(screen, font)
        text_surface = font.render(button_instructions[button.text], True, (0, 0, 0))
        instruction_x = button.rect.right + 10  # Padding to the right of the button
        instruction_y = button.rect.y + (button.rect.height // 2 - text_surface.get_height() // 2)  # Center vertically

        # Ensure instructions do not overflow the screen width
        if instruction_x + text_surface.get_width() > SCREEN_WIDTH:
            instruction_x = button.rect.x - text_surface.get_width() - 10  # Move to the left side of the button

        screen.blit(text_surface, (instruction_x, instruction_y))

    # Draw slider
    pygame.draw.rect(screen, (200, 200, 200), controls["slider_rect"])
    pygame.draw.circle(
        screen, (0, 0, 255),
        (controls["slider_knob_x"], controls["slider_rect"].y + controls["slider_rect"].height // 2),
        10
    )

    # Calculate speed factor dynamically
    slider_fraction = (controls["slider_knob_x"] - controls["slider_x"]) / controls["slider_width"]
    speed_factor = round(1 + slider_fraction * 49, 1)  # Speed range: 1x–50x
    state["speed_factor"] = speed_factor
    state["speed"] = int(INITIAL_DELAY / speed_factor)  # Adjust speed dynamically


    # Display speed label
    speed_label = font.render(f"Speed: {speed_factor:.1f}x", True, (0, 0, 0))
    screen.blit(speed_label, (controls["slider_x"], controls["slider_rect"].y + controls["slider_rect"].height + 10))

    # Draw quit instructions
    quit_text = font.render("Press ESC or close the window to quit.", True, (0, 0, 0))
    quit_text_y = controls["slider_rect"].y + controls["slider_rect"].height + 30  # Below the speed label
    screen.blit(quit_text, (controls["slider_x"], quit_text_y))
