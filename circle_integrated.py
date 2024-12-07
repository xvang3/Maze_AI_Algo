import sys
import math
import threading
import pygame
from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class SliderApp(QWidget):
    def __init__(self, shared_data):
        super().__init__()
        self.shared_data = shared_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyQt Slider for Pygame")

        # Create a slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)  # Minimum speed
        self.slider.setMaximum(50)  # Maximum speed
        self.slider.setValue(10)  # Default value
        self.slider.valueChanged.connect(self.on_slider_change)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def on_slider_change(self):
        # Update shared speed value
        self.shared_data["speed"] = self.slider.value() / 10.0  # Scale speed


def run_pygame(shared_data):
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Circle Controlled by PyQt Slider")

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Clock
    clock = pygame.time.Clock()

    # Circle parameters
    circle_center = (WIDTH // 2, HEIGHT // 2)
    circle_radius = 100
    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(WHITE)

        # Update the angle based on shared speed
        angle += shared_data["speed"]
        if angle >= 360:
            angle -= 360

        # Calculate circle position
        circle_x = circle_center[0] + circle_radius * math.cos(math.radians(angle))
        circle_y = circle_center[1] + circle_radius * math.sin(math.radians(angle))

        # Draw the circle
        pygame.draw.circle(screen, RED, (int(circle_x), int(circle_y)), 10)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


def main():
    # Shared data between PyQt and Pygame
    shared_data = {"speed": 1.0}  # Default speed

    # Run Pygame in a separate thread
    pygame_thread = threading.Thread(target=run_pygame, args=(shared_data,))
    pygame_thread.start()

    # Run PyQt in the main thread
    app = QApplication(sys.argv)
    slider_app = SliderApp(shared_data)
    slider_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
