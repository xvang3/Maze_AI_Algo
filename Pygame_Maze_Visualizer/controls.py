from button import Button
import pygame
from maze_generator import generate_random_maze_with_solution
from settings import *

# Constant for number of buttons
NUM_BUTTONS = 6
OTHER_SETTINGS = 2
TOTAL_BUTTONS = NUM_BUTTONS + OTHER_SETTINGS


# Constants for UI layout
SLIDER_WIDTH = 200  # Slider width
SLIDER_HEIGHT = 20
SLIDER_MIN = 0.1  # Minimum speed factor
SLIDER_MAX = 50.0  # Maximum speed factor
BUTTONS_BOTTOM_MARGIN = 100  # Space between the last button and the slider

def init_controls(maze_width, rows, cols, state, offset_x=0, offset_y=0):
    """Initialize UI control components with proper alignment."""
    # Define the bounding box for all controls
    control_box_x = 20
    control_box_y = SCREEN_HEIGHT - 250  # Start positioning higher to leave space for controls
    control_box_width = 420
    control_box_height = 220

    # Define button actions
    def start_action():
        if state["started"]:  # Ignore clicks if already running
            return
        state["started"] = True
        state["state_label"] = "Running"
        if "create_generator" in state:
            state["algorithm_generator"] = state["create_generator"]()  # Create a fresh generator



    def pause_action():
        if state["started"]:
            state["paused"] = not state["paused"]
            state["state_label"] = "Paused" if state["paused"] else "Running"

    def stop_action():
        if not state["stop_clicked"]:
            state["started"] = False
            state["state_label"] = "Stopped"
            state["stop_clicked"] = True
        else:
            state["current_node"] = None
            state["visited_nodes"].clear()
            state["solution_path"] = []
            state["state_label"] = "Reset"
            state["stop_clicked"] = False


    def new_maze_action():
        state["maze"] = generate_random_maze_with_solution(rows, cols) #removed wall_density=0.3
        state["started"] = False
        state["current_node"] = None
        state["visited_nodes"] = set()
        state["solution_path"] = []
        if "create_generator" in state:
            state["algorithm_generator"] = state["create_generator"]()  # Create a fresh generator



    def reset_speed_action():
        state["speed_factor"] = 1.0  # Reset to 1x speed
        controls["slider_knob_x"] = controls["slider_x"] + (SLIDER_WIDTH // 2)  # Center knob visually
        state["speed"] = int(INITIAL_DELAY / state["speed_factor"])  # Reset the speed factor

    def back_action(state):
        state["in_selection"] = True  # Set in_selection to True to return to the selection menu
        state["running"] = False      # Stop the current loop



    def x2_speed_action():
        state["speed_factor"] = min(SLIDER_MAX, state["speed_factor"] * 2)  # Double the speed
        controls["slider_knob_x"] = controls["slider_x"] + int(
            controls["slider_width"] * ((state["speed_factor"] - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN))
        )

    def divide2_speed_action():
        state["speed_factor"] = max(SLIDER_MIN, state["speed_factor"] / 2)  # Halve the speed
        controls["slider_knob_x"] = controls["slider_x"] + int(
            controls["slider_width"] * ((state["speed_factor"] - SLIDER_MIN) / (SLIDER_MAX - SLIDER_MIN))
        )

    # Define relative positions inside the control box
    button_x = control_box_x + 10
    button_y = control_box_y + 10
    slider_x = control_box_x + 10
    slider_y = control_box_y + 170  # Positioned below buttons

    # Adjust button size and spacing
    button_width, button_height = 100, 20
    button_spacing = 25

    # Create buttons
    buttons = [
        Button(button_x, button_y, button_width, button_height, "Start", (50, 205, 50), (0, 0, 0), start_action),
        Button(button_x, button_y + button_spacing, button_width, button_height, "Pause/Resume", (135, 206, 235), (0, 0, 0), pause_action),
        Button(button_x, button_y + button_spacing * 2, button_width, button_height, "Stop", (220, 20, 60), (255, 255, 255), stop_action),
        Button(button_x, button_y + button_spacing * 3, button_width, button_height, "New Maze", (65, 105, 225), (255, 255, 255), new_maze_action),
        Button(button_x + 120, button_y, button_width, button_height, "Reset Speed", (255, 215, 0), (0, 0, 0), reset_speed_action),
        Button(button_x + 120, button_y + button_spacing, button_width, button_height, "Back", (255, 140, 0), (0, 0, 0), lambda: back_action(state)),        
        Button(slider_x + SLIDER_WIDTH + 20, slider_y, 40, SLIDER_HEIGHT, "÷2", (112, 128, 144), (255, 255, 255), divide2_speed_action),
        Button(slider_x + SLIDER_WIDTH + 70, slider_y, 40, SLIDER_HEIGHT, "x2", (112, 128, 144), (255, 255, 255), x2_speed_action),
    ]

    # Initialize slider
    slider_rect = pygame.Rect(slider_x, slider_y, SLIDER_WIDTH, SLIDER_HEIGHT)
    controls = {
        "buttons": buttons,
        "slider_rect": slider_rect,
        "slider_knob_x": slider_x + (SLIDER_WIDTH // 2),  # Start in the middle (1x speed)
        "slider_x": slider_x,
        "slider_width": SLIDER_WIDTH,
        "control_box_rect": pygame.Rect(control_box_x, control_box_y, control_box_width, control_box_height),
        "slider_dragging": False,  # Track if slider knob is being dragged
    }

    # Set initial speed factor
    state["speed_factor"] = 1.0
    return controls


def draw_controls(screen, controls, state, font):
    """Draw controls with a slider, buttons, and instructions."""
    # Draw the control box
    pygame.draw.rect(screen, (173, 216, 230), controls["control_box_rect"])  # Light blue background
    pygame.draw.rect(screen, (0, 102, 204), controls["control_box_rect"], 2)  # Dark blue border

    # Draw buttons
    for button in controls["buttons"]:
        if button.text == "Start" and state["started"]:
            button.color = (169, 169, 169)  # Gray for disabled
        elif button.text == "Pause/Resume" and not state["started"]:
            button.color = (169, 169, 169)  # Gray for disabled
        else:
            button.color = button.default_color  # Reset to default
        button.draw(screen, font)

    # Draw slider
    pygame.draw.rect(screen, (0, 0, 0), controls["slider_rect"])
    pygame.draw.circle(
        screen, (0, 0, 255),
        (controls["slider_knob_x"], controls["slider_rect"].y + controls["slider_rect"].height // 2),
        10
    )

    # Calculate speed factor dynamically
    slider_fraction = (controls["slider_knob_x"] - controls["slider_x"]) / controls["slider_width"]
    state["speed_factor"] = round(SLIDER_MIN + slider_fraction * (SLIDER_MAX - SLIDER_MIN), 1)
    state["speed"] = int(INITIAL_DELAY / state["speed_factor"])  # Ensure speed is an integer


    # Display speed label
    speed_label = font.render(f"Speed: {state['speed_factor']:.1f}x", True, (0, 0, 0))
    screen.blit(speed_label, (controls["slider_x"], controls["slider_rect"].y - 25))

    # Draw slider instructions below the slider
    slider_instructions = font.render("Adjust slider to change speed.", True, (0, 0, 0))
    slider_instructions_y = controls["slider_rect"].y + controls["slider_rect"].height + 10
    screen.blit(slider_instructions, (controls["slider_x"], slider_instructions_y))

    # Draw the algorithm label (BFS, DFS, Heuristic, A*)
    algorithm_label = font.render(f"Algorithm: {state['algorithm']}", True, (0, 0, 0))
    algorithm_label_x = controls["control_box_rect"].x + 10
    algorithm_label_y = controls["control_box_rect"].y - 50  # Position above the state label
    screen.blit(algorithm_label, (algorithm_label_x, algorithm_label_y))

    # Display state label
    state_label_surface = font.render(f"State: {state['state_label']}", True, (0, 0, 0))
    state_label_x = controls["control_box_rect"].x + 10
    state_label_y = controls["control_box_rect"].y - 30  # Position above the control box
    screen.blit(state_label_surface, (state_label_x, state_label_y))



def handle_slider_event(event, controls, state):
    """Handle slider dragging and clicking."""
    # Handle mouse press
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if the click is on the knob or anywhere on the slider
        if controls["slider_rect"].collidepoint(event.pos) or (
            abs(event.pos[0] - controls["slider_knob_x"]) <= 10
        ):
            controls["slider_dragging"] = True
            # Update the knob position immediately to the click location
            controls["slider_knob_x"] = min(
                max(event.pos[0], controls["slider_x"]), 
                controls["slider_x"] + controls["slider_width"]
            )

    # Handle mouse release
    if event.type == pygame.MOUSEBUTTONUP:
        controls["slider_dragging"] = False

    # Handle mouse motion
    if event.type == pygame.MOUSEMOTION and controls["slider_dragging"]:
        # Move the knob as the mouse moves
        controls["slider_knob_x"] = min(
            max(event.pos[0], controls["slider_x"]),
            controls["slider_x"] + controls["slider_width"]
        )




