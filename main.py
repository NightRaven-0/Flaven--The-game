import pygame
import random
import sys
import os
from bird import Bird
from pipe import Pipe
import config
import time
import game_end

pygame.init()

# Initialize screen
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Flaven")
icon = pygame.image.load('assets/images/flaven_icon.png')
pygame.display.set_icon(icon)
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

# Load number images
number_images = [pygame.image.load(f'assets/images/{i}.png') for i in range(10)]

# Fonts for text rendering (we might not use this for score anymore)
font = pygame.font.SysFont('Arial', 30)

def draw_score(screen, score):
    """Draw the score using number images at the top center."""
    score_str = str(score)
    total_width = 0
    for digit in score_str:
        total_width += number_images[int(digit)].get_width()

    x_offset = (config.SCREEN_WIDTH - total_width) // 2
    for digit in score_str:
        image = number_images[int(digit)]
        screen.blit(image, (x_offset, 50)) # Adjust the vertical position as needed
        x_offset += image.get_width()

def game_loop():
    global selected_bird
    selected_bird = 'blue'  # Default bird selection

    flaven = Bird(100, config.SCREEN_HEIGHT // 2, bird_images[selected_bird])

    pipes = []
    ground_x = 0
    score = 0
    game_over = False
    last_pipe_x = config.SCREEN_WIDTH + 300
    passed_pipe_index = -1

    # Day/Night cycle variables
    current_background = background_day
    cycle_timer = random.uniform(30, 50)  # Get a random time between 30 and 50 seconds
    last_cycle_time = time.time()

    def reset_game():
        nonlocal pipes, ground_x, score, game_over, last_pipe_x, passed_pipe_index, cycle_timer, last_cycle_time, flaven
        flaven = Bird(100, config.SCREEN_HEIGHT // 2, bird_images[selected_bird])
        pipes = []
        ground_x = 0
        score = 0
        game_over = False
        last_pipe_x = config.SCREEN_WIDTH + 300
        passed_pipe_index = -1
        cycle_timer = random.uniform(30, 50)
        last_cycle_time = time.time()
        # Initial pipe creation
        ground_height = ground_img.get_height()
        gap_height = 150
        max_top_pipe_bottom = config.SCREEN_HEIGHT - ground_height - gap_height - 50
        if max_top_pipe_bottom < 50:
            max_top_pipe_bottom = 50
        top_pipe_bottom = random.randint(50, max_top_pipe_bottom)
        bottom_pipe_top = top_pipe_bottom + gap_height
        pipes.append(Pipe(last_pipe_x, top_pipe_bottom, bottom_pipe_top))

    # Initial pipe creation
    ground_height = ground_img.get_height()
    gap_height = 150
    max_top_pipe_bottom = config.SCREEN_HEIGHT - ground_height - gap_height - 50
    if max_top_pipe_bottom < 50:
        max_top_pipe_bottom = 50
    top_pipe_bottom = random.randint(50, max_top_pipe_bottom)
    bottom_pipe_top = top_pipe_bottom + gap_height
    pipes.append(Pipe(last_pipe_x, top_pipe_bottom, bottom_pipe_top))

    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key in game_end.bird_colors:
                        selected_bird = game_end.bird_colors[event.key].lower()
                        game_end.set_selection_message(game_end.bird_colors[event.key])
                    elif event.key == pygame.K_r:
                        reset_game()
                elif event.key == pygame.K_SPACE and not game_over:
                    flaven.flap()
                elif not game_over:
                    if event.key in game_end.bird_colors:
                        selected_bird = game_end.bird_colors[event.key].lower()
                        flaven.image = bird_images[selected_bird]

        if game_over:
            game_end.game_over_screen(screen, font, game_over_img)
        else:
            # Update background (Day/Night Cycle)
            current_time = time.time()
            if current_time - last_cycle_time >= cycle_timer:
                if current_background == background_day:
                    current_background = background_night
                else:
                    current_background = background_day
                cycle_timer = random.uniform(30, 50)  # Reset the timer with a new random value
                last_cycle_time = current_time

            screen.blit(current_background, (0, 0))

            # Get the time delta for smooth updates
            dt = clock.get_time() / 1000  # Get time in seconds

            # Update the bird
            flaven.update(dt)

            # Update pipes and handle collisions
            for i, pipe in enumerate(pipes):
                pipe.update(dt)  # Pass the delta time for smooth movement
                pipe.draw(screen)

                if pipe.top_rect.colliderect(flaven.rect) or pipe.bottom_rect.colliderect(flaven.rect):
                    game_over = True

                # Check for score
                if flaven.rect.left > pipe.top_rect.right and i > passed_pipe_index:
                    score += 1
                    passed_pipe_index = i

            # Remove off-screen pipes
            if pipes and pipes[0].x < -pipes[0].width:
                pipes.pop(0)
                # Reset passed_pipe_index when a pipe is removed
                passed_pipe_index = -1 if len(pipes) == 0 else max(0, passed_pipe_index -1)

            # Add new pipes more frequently
            if not game_over and len(pipes) > 0 and pipes[-1].x < config.SCREEN_WIDTH - 500: # Adjust this value to control frequency
                ground_height = ground_img.get_height()
                gap_height = 150
                max_top_pipe_bottom = config.SCREEN_HEIGHT - ground_height - gap_height - 50
                if max_top_pipe_bottom < 50:
                    max_top_pipe_bottom = 50
                top_pipe_bottom = random.randint(50, max_top_pipe_bottom)
                bottom_pipe_top = top_pipe_bottom + gap_height
                new_pipe = Pipe(config.SCREEN_WIDTH, top_pipe_bottom, bottom_pipe_top)
                pipes.append(new_pipe)

            # Check if the bird collides with the ground
            if flaven.rect.bottom >= config.SCREEN_HEIGHT - ground_img.get_height():
                game_over = True

            # Draw the bird
            flaven.draw(screen)

            # Draw the ground (looping)
            ground_width = ground_img.get_width()
            screen.blit(ground_img, (ground_x, config.SCREEN_HEIGHT - ground_img.get_height()))
            screen.blit(ground_img, (ground_x + ground_width, config.SCREEN_HEIGHT - ground_img.get_height()))

            # Scroll the ground
            ground_x -= config.PIPE_SPEED * dt
            if ground_x <= -ground_width:
                ground_x = 0

            # Draw score using custom images
            draw_score(screen, score)

        # Refresh the display
        pygame.display.update()
        clock.tick(config.FPS)

if __name__ == "__main__":
    game_loop()