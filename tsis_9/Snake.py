import pygame
import random
import sys

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 30

# Game-level settings
FOOD_COUNT_FOR_LEVEL_UP = 4
INITIAL_SPEED = 5
LEVEL_SPEED_INCREMENT = 2

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (50, 50, 50)

# We'll use different colors depending on the food weight
FOOD_COLORS = {
    1: (255, 0, 0),      # Red
    2: (255, 165, 0),    # Orange
    3: (255, 255, 0),    # Yellow
    4: (0, 255, 255),    # Cyan
    5: (255, 0, 255)     # Magenta
}

def draw_snake(surface, snake_body):
    """Draws the snake on the given surface."""
    for segment in snake_body:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def get_random_position(snake_body):
    """
    Returns a (x, y) position for food such that it doesn't overlap
    with the snake's body.
    """
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if (x, y) not in snake_body:
            return (x, y)

def spawn_food(snake_body):
    """
    Creates a food dictionary with random position,
    random weight (1 to 5), a creation time, and a lifetime (in ms).
    """
    position = get_random_position(snake_body)
    weight = random.randint(1, 5)
    color = FOOD_COLORS[weight]
    
    # Lifetime (in ms) can be random or fixed. Here we make it random between 3–6 seconds.
    lifetime = random.randint(3000, 6000)
    creation_time = pygame.time.get_ticks()  # Current time in ms
    
    return {
        "pos": position,
        "weight": weight,
        "color": color,
        "creation_time": creation_time,
        "lifetime": lifetime
    }

def display_text(surface, text, font, color, x, y):
    """Utility to display text on the given surface."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with Timed, Weighted Food")

    clock = pygame.time.Clock()

    # Font for score and level display
    font = pygame.font.SysFont(None, 30)

    # Initial snake setup
    snake_body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # List of (x, y)
    direction = "RIGHT"  # Possible directions: UP, DOWN, LEFT, RIGHT

    # Spawn our first (and only) piece of food
    current_food = spawn_food(snake_body)

    # Game stats
    score = 0
    level = 1
    food_eaten_current_level = 0

    # Game speed (cells per tick); movement update is decoupled from the FPS
    snake_speed = INITIAL_SPEED
    move_counter = 0  # Will increment each frame, used to determine when to move snake

    running = True
    while running:
        # --------------------- EVENT HANDLING ---------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        move_counter += 1
        if move_counter >= (FPS // snake_speed):
            move_counter = 0
            head_x, head_y = snake_body[0]

            if direction == "UP":
                head_y -= BLOCK_SIZE
            elif direction == "DOWN":
                head_y += BLOCK_SIZE
            elif direction == "LEFT":
                head_x -= BLOCK_SIZE
            elif direction == "RIGHT":
                head_x += BLOCK_SIZE

            new_head = (head_x, head_y)

            # Check boundaries
            if (head_x < 0 or head_x >= SCREEN_WIDTH or 
                head_y < 0 or head_y >= SCREEN_HEIGHT):
                running = False
            else:
                # Check self-collision
                if new_head in snake_body:
                    running = False
                else:
                    snake_body.insert(0, new_head)
                    
                    # Check if we eat the food
                    if new_head == current_food["pos"]:
                        # Increase score by the weight of the food
                        score += current_food["weight"]
                        food_eaten_current_level += 1
                        
                        # Check level-up
                        if food_eaten_current_level >= FOOD_COUNT_FOR_LEVEL_UP:
                            level += 1
                            food_eaten_current_level = 0
                            snake_speed += LEVEL_SPEED_INCREMENT
                        
                        # Spawn new food
                        current_food = spawn_food(snake_body)
                    else:
                        # Normal movement, pop the tail
                        snake_body.pop()
        
        # Check if current food has expired
        now = pygame.time.get_ticks()
        if now - current_food["creation_time"] > current_food["lifetime"]:
            # Food has expired, spawn a new one
            current_food = spawn_food(snake_body)

        screen.fill(BLACK)

        # Draw the current food
        pygame.draw.rect(
            screen, 
            current_food["color"], 
            (current_food["pos"][0], current_food["pos"][1], BLOCK_SIZE, BLOCK_SIZE)
        )

        # Draw the snake
        draw_snake(screen, snake_body)

        # Display score and level
        display_text(screen, f"Score: {score}", font, WHITE, 10, 10)
        display_text(screen, f"Level: {level}", font, WHITE, 10, 40)

        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(screen, font, score, level)
    pygame.quit()
    sys.exit()

def game_over_screen(surface, font, score, level):
    """Displays a simple 'Game Over' screen."""
    surface.fill(BLACK)
    display_text(surface, "GAME OVER", font, (200, 0, 0), SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20)
    display_text(surface, f"Final Score: {score}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 10)
    display_text(surface, f"Level Reached: {level}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40)
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds

if __name__ == "__main__":
    main()
