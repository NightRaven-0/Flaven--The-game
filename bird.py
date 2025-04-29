import pygame
import os
import config

class Bird:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -10
        self.flap_strength = 10

    def update(self, dt):
        """Update the bird's position with gravity and velocity."""
        self.velocity += self.gravity  # Apply gravity
        self.y += self.velocity  # Move bird down with velocity
        self.rect.center = (self.x, self.y)

        # Prevent the bird from falling below the screen (ground collision)
        if self.y >= config.SCREEN_HEIGHT - self.rect.height // 2:
            self.y = config.SCREEN_HEIGHT - self.rect.height // 2
            self.velocity = 0  # Stop downward velocity upon ground hit

        # Prevent the bird from going above the screen (ceiling collision)
        if self.y <= 0 + self.rect.height // 2:
            self.y = 0 + self.rect.height // 2
            self.velocity = 0  # Stop upward velocity upon ceiling hit

    def draw(self, screen):
        """Draw the bird on the screen."""
        screen.blit(self.image, self.rect)

    def flap(self):
        """Make the bird flap."""
        self.velocity = self.lift  # Apply lift to the bird
