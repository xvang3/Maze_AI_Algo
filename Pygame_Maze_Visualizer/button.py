import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.default_color = color
        self.hover_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))  # Lighter color for hover

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):  # Check if mouse is over the button
            pygame.draw.rect(screen, (50, 50, 50), self.rect.inflate(10, 10))  # Shadow effect
            pygame.draw.rect(screen, self.hover_color, self.rect)  # Change color on hover
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Draw text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
