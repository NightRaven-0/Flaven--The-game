import pygame
import os

class Pipe:
    def __init__(self, x, height):
        self.x = x  # X position of the pipe
        self.height = height  # Height of the top pipe
        self.width = 80  # Width of the pipe
        self.gap = 200  # The gap between the top and bottom pipes

        # Load pipe images (Make sure these are in the correct path)
        self.top_img = pygame.image.load(os.path.join('assets', 'images', 'pipe_top.png'))
        self.bottom_img = pygame.image.load(os.path.join('assets', 'images', 'pipe_bottom.png'))

        # Get the rectangles for collision detection
        self.top_rect = self.top_img.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = self.bottom_img.get_rect(midtop=(self.x, self.height + self.gap))

    def update(self, dt):
        """Move the pipe to the left based on time delta."""
        self.x -= 200 * dt  # Adjust speed of the pipe (200 pixels per second)
        
        # Update the positions of the pipe rectangles
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        """Draw the pipes on the screen."""
        screen.blit(self.top_img, self.top_rect)
        screen.blit(self.bottom_img, self.bottom_rect)
