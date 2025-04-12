import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Squid Game: Red Light, Green Light")

# Colors
SAND = (194, 178, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
BUTTON_COLOR = (0, 128, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
player_pos = [50, HEIGHT // 2]  # Human player's starting position
computer_players = [[50, HEIGHT // 10 + (i + 1) * 60] for i in range(10)]  # 10 AI players
finish_line = WIDTH - 100  # Finish line position
light = "Green"  # Current light state
move_allowed = True  # Whether movement is allowed
game_over = False  # Game state
clock = pygame.time.Clock()

# Light change variables
light_change_interval = 3000  # Light changes every 3 seconds
last_light_change = pygame.time.get_ticks()  # Time of last light change

# Traffic light variables
light_box_x = WIDTH - 100  # X-coordinate for the traffic light box
light_box_y = 5  # Y-coordinate for the traffic light box
light_box_width = 60  # Width of the traffic light box
light_box_height = 150  # Height of the traffic light box
light_radius = 20  # Radius of the traffic light circles

# Load images
try:
    player_image = pygame.image.load("player.png").convert_alpha()  # Replace with your player image
    doll_image = pygame.image.load("doll.png").convert_alpha()  # Replace with your doll image
    computer_image = pygame.image.load("player.png").convert_alpha()  # Image for computer players
except FileNotFoundError:
    print("Error: Image files not found. Please ensure 'player.png' and 'doll.png' are in the same directory.")
    sys.exit()

# Resize images
player_image = pygame.transform.scale(player_image, (50, 50))
doll_image = pygame.transform.scale(doll_image, (100, 200))
computer_image = pygame.transform.scale(computer_image, (50, 50))

def draw_traffic_light():
    """Draw the traffic light box and lights."""
    pygame.draw.rect(screen, GRAY, (light_box_x, light_box_y, light_box_width, light_box_height))
    pygame.draw.circle(screen, RED if light == "Red" else BLACK, (light_box_x + light_box_width // 2, light_box_y + 40), light_radius)
    pygame.draw.circle(screen, GREEN if light == "Green" else BLACK, (light_box_x + light_box_width // 2, light_box_y + 110), light_radius)

def draw_objects():
    """Draw all game objects on the screen."""
    screen.fill(SAND)

    # Draw finish line
    pygame.draw.line(screen, BLACK, (finish_line, 0), (finish_line, HEIGHT), 5)

    # Draw human player
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    # Draw computer players
    for pos in computer_players:
        screen.blit(computer_image, (pos[0], pos[1]))

    # Draw doll
    screen.blit(doll_image, (WIDTH // 5 + 550, HEIGHT // 4))

    # Draw traffic light
    draw_traffic_light()

    # Display instructions
    instructions = font.render("Press SPACE to move", True, BLACK)
    screen.blit(instructions, (10, 10))
    pygame.display.flip()

def check_collision():
    """Check if any player has reached the finish line."""
    global game_over

    # Check human player
    if player_pos[0] >= finish_line:
        game_over = True
        return "human_win"

    # Check computer players
    for i, pos in enumerate(computer_players):
        if pos[0] >= finish_line:
            game_over = True
            return f"computer_{i}_win"

    return None

def display_message(message):
    """Display a win/lose message on the screen."""
    screen.fill(SAND)
    text = font.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing

def draw_main_menu():
    """Draw the main menu."""
    screen.fill(SAND)
    title = font.render("Squid Game: Red Light, Green Light", True, BLACK)
    new_game_button = font.render("1 - New Game", True, BUTTON_COLOR)
    quit_button = font.render("2 - Quit", True, BUTTON_COLOR)
    screen.blit(title, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
    screen.blit(new_game_button, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(quit_button, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.flip()

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return  # Start a new game
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def reset_game():
    """Reset the game variables to their initial state."""
    global player_pos, computer_players, light, move_allowed, game_over, last_light_change
    player_pos = [50, HEIGHT // 2]
    computer_players = [[50, HEIGHT // 10 + (i + 1) * 60] for i in range(10)]
    light = "Green"
    move_allowed = True
    game_over = False
    last_light_change = pygame.time.get_ticks()

def main():
    global player_pos, light, move_allowed, game_over, last_light_change, computer_players

    while True:
        # Show the main menu
        main_menu()

        # Reset the game state
        reset_game()

        # Main game loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if it's time to change the light
            current_time = pygame.time.get_ticks()
            if current_time - last_light_change >= light_change_interval:
                light = "Red" if light == "Green" else "Green"
                move_allowed = light == "Green"
                last_light_change = current_time  # Reset the timer

            # Move human player if allowed
            keys = pygame.key.get_pressed()
            if move_allowed and keys[pygame.K_SPACE]:
                player_pos[0] += 5

            # Check if the human player moves during Red Light
            if not move_allowed and keys[pygame.K_SPACE]:
                game_over = True
                display_message("You Lose! You moved during Red Light!")
                break

            # Move computer players if allowed
            if move_allowed:
                for i in range(len(computer_players)):
                    computer_players[i][0] += random.randint(1, 5)  # Random movement

            # Draw objects
            draw_objects()

            # Check for win conditions
            result = check_collision()
            if result:
                if result == "human_win":
                    display_message("You Win! Congratulations!")
                else:
                    display_message(f"Computer {result.split('_')[1]} wins!")
                break

            clock.tick(30)  # Limit to 30 FPS

if __name__ == "__main__":
    main()