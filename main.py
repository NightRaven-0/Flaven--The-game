import pygame
import random
import sys
import os
from bird import Bird
from pipe import Pipe
import config

pygame.init()

# Initialize screen
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Flaven")
clock = pygame.time.Clock()

# Load images (update file paths as necessary)
background_day = pygame.image.load('assets/images/background_day.png')
background_night = pygame.image.load('assets/images/background_night.png')
ground_img = pygame.image.load('assets/images/ground.png')
game_over_img = pygame.image.load('assets/images/game_over.png')  # Your custom game over PNG
bird_images = {
    'blue': pygame.image.load('assets/images/blue_bird.png'),
    'yellow': pygame.image.load('assets/images/yellow_bird.png'),
    'red': pygame.image.load('assets/images/red_bird.png'),
    'black': pygame.image.load('assets/images/black_bird.png')
}

# Fonts for text rendering
font = pygame.font.SysFont('Arial', 30)

def game_over_screen():
    """Displays the Game Over screen with the custom PNG."""
    screen.blit(game_over_img, (config.SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, config.SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))

    bird_select_text = font.render("Press 1 for Blue, 2 for Yellow, 3 for Red, 4 for Black", True, (255, 255, 255))
    screen.blit(bird_select_text, (config.SCREEN_WIDTH // 2 - bird_select_text.get_width() // 2, config.SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()

def game_loop():
    global selected_bird
    selected_bird = 'blue'  # Default bird selection

    flaven = Bird(100, config.SCREEN_HEIGHT // 2, bird_images[selected_bird])
    
    pipes = [Pipe(config.SCREEN_WIDTH + 300, random.randint(config.SCREEN_HEIGHT // 2, config.SCREEN_HEIGHT - 100))]
    
    ground_x = 0
    score = 0
    game_over = False
    
    while True:
        screen.fill((255, 255, 255))  # Fill with white for now

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    flaven.flap()
                if event.key == pygame.K_1:
                    selected_bird = 'blue'
                elif event.key == pygame.K_2:
                    selected_bird = 'yellow'
                elif event.key == pygame.K_3:
                    selected_bird = 'red'
                elif event.key == pygame.K_4:
                    selected_bird = 'black'

        if game_over:
            game_over_screen()  # Show Game Over screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game when 'R' is pressed
                        game_loop()  # Recursively restart the game

        # Update background (Toggle between day and night)
        if not game_over:
            screen.blit(background_day, (0, 0))
        
        # Get the time delta for smooth updates
        dt = clock.get_time() / 1000  # Get time in seconds
        
        # Update the bird
        flaven.update(dt)
        
        # Update pipes and handle collisions
        for pipe in pipes:
            pipe.update(dt)  # Pass the delta time for smooth movement
            pipe.draw(screen)
            
            if pipe.top_rect.colliderect(flaven.rect) or pipe.bottom_rect.colliderect(flaven.rect):
                game_over = True

        # Remove off-screen pipes and add new ones
        if pipes[0].x < -pipes[0].width:
            pipes.pop(0)
            pipes.append(Pipe(config.SCREEN_WIDTH, random.randint(config.SCREEN_HEIGHT // 2, config.SCREEN_HEIGHT - 200)))  # Ensure pipes are higher up
            
            score += 1
        
        # Check if the bird collides with the ground
        if flaven.rect.bottom >= config.SCREEN_HEIGHT - ground_img.get_height():
            game_over = True
        
        # Draw the bird
        flaven.draw(screen)
        
        # Draw the ground
        screen.blit(ground_img, (ground_x, config.SCREEN_HEIGHT - ground_img.get_height()))
        
        # Scroll the ground
        ground_x -= 5
        if ground_x <= -config.SCREEN_WIDTH:
            ground_x = 0
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Refresh the display
        pygame.display.update()

        clock.tick(config.FPS)

if __name__ == "__main__":
    game_loop()
