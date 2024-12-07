import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slider Example: Adjust Speed")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Circle parameters
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 100
angle = 0

# Slider parameters
slider_x = 50
slider_y = HEIGHT - 50
slider_width = 500
slider_height = 10
slider_knob_radius = 10
slider_knob_x = slider_x

# Speed parameters
speed_min = 0.1
speed_max = 5
speed = speed_min

# Quit button parameters
button_rect = pygame.Rect(WIDTH - 100, 10, 80, 30)

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                running = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button held down
                mouse_x, _ = event.pos
                if slider_x <= mouse_x <= slider_x + slider_width:
                    slider_knob_x = mouse_x
                    # Map slider position to speed
                    slider_position = (slider_knob_x - slider_x) / slider_width
                    speed = speed_min + slider_position * (speed_max - speed_min)

    # Update the angle based on speed
    angle += speed
    if angle >= 360:
        angle -= 360

    # Calculate circle position
    circle_x = circle_center[0] + circle_radius * math.cos(math.radians(angle))
    circle_y = circle_center[1] + circle_radius * math.sin(math.radians(angle))

    # Draw the circle
    pygame.draw.circle(screen, RED, (int(circle_x), int(circle_y)), 10)

    # Draw the slider
    pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, BLUE, (int(slider_knob_x), slider_y + slider_height // 2), slider_knob_radius)

    # Draw the quit button
    pygame.draw.rect(screen, RED, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Quit", True, WHITE)
    screen.blit(text, (button_rect.x + 20, button_rect.y + 5))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
