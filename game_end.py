# game_end.py
import pygame
import config

bird_colors = {
    pygame.K_1: "Blue",
    pygame.K_2: "Yellow",
    pygame.K_3: "Red",
    pygame.K_4: "Black"
}

selection_message = ""
message_timer = 0
MESSAGE_DURATION = 1500  # milliseconds

def set_selection_message(color):
    global selection_message, message_timer
    selection_message = f"{color} bird selected!"
    message_timer = pygame.time.get_ticks()

def game_over_screen(screen, font, game_over_img):
    """Displays the Game Over screen with the custom PNG and options."""
    global selection_message  # Declare selection_message as global at the start
    screen.fill((0, 0, 0))  # Fill the screen with black
    game_over_rect = game_over_img.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_img, game_over_rect)

    controls_text = font.render("1: Blue, 2: Yellow, 3: Red, 4: Black, Q: Quit, R: Restart", True, (255, 255, 255))
    controls_rect = controls_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + game_over_img.get_height() // 2 + 30))
    screen.blit(controls_text, controls_rect)

    current_time = pygame.time.get_ticks()
    if selection_message and current_time < message_timer + MESSAGE_DURATION:
        message_text = font.render(selection_message, True, (0, 255, 0))  # Green message
        message_rect = message_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + game_over_img.get_height() + 70))
        screen.blit(message_text, message_rect)
    elif current_time >= message_timer + MESSAGE_DURATION:
        selection_message = ""

    pygame.display.update()

    return selection_message # Return the message for potential use in main.py (though not strictly needed here)