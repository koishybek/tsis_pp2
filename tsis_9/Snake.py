import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 30

FOOD_COUNT_FOR_LEVEL_UP = 4
INITIAL_SPEED = 5
LEVEL_SPEED_INCREMENT = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (50, 50, 50)

FOOD_COLORS = {
    1: (255, 0, 0),
    2: (255, 165, 0),
    3: (255, 255, 0),
    4: (0, 255, 255),
    5: (255, 0, 255)
}

def draw_snake(surface, snake_body):
    for segment in snake_body:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def get_random_position(snake_body):
    while True:
        x = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if (x, y) not in snake_body:
            return (x, y)

def spawn_food(snake_body):
    position = get_random_position(snake_body)
    weight = random.randint(1, 5)
    color = FOOD_COLORS[weight]
    lifetime = random.randint(3000, 6000)
    creation_time = pygame.time.get_ticks()
    return {
        "pos": position,
        "weight": weight,
        "color": color,
        "creation_time": creation_time,
        "lifetime": lifetime
    }

def display_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with Timed, Weighted Food")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    snake_body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    direction = "RIGHT"
    current_food = spawn_food(snake_body)
    score = 0
    level = 1
    food_eaten_current_level = 0
    snake_speed = INITIAL_SPEED
    move_counter = 0
    running = True

    while running:
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

            if (head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT):
                running = False
            else:
                if new_head in snake_body:
                    running = False
                else:
                    snake_body.insert(0, new_head)
                    if new_head == current_food["pos"]:
                        score += current_food["weight"]
                        food_eaten_current_level += 1
                        if food_eaten_current_level >= FOOD_COUNT_FOR_LEVEL_UP:
                            level += 1
                            food_eaten_current_level = 0
                            snake_speed += LEVEL_SPEED_INCREMENT
                        current_food = spawn_food(snake_body)
                    else:
                        snake_body.pop()

        now = pygame.time.get_ticks()
        if now - current_food["creation_time"] > current_food["lifetime"]:
            current_food = spawn_food(snake_body)

        screen.fill(BLACK)
        pygame.draw.rect(screen, current_food["color"], (current_food["pos"][0], current_food["pos"][1], BLOCK_SIZE, BLOCK_SIZE))
        draw_snake(screen, snake_body)
        display_text(screen, f"Score: {score}", font, WHITE, 10, 10)
        display_text(screen, f"Level: {level}", font, WHITE, 10, 40)
        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(screen, font, score, level)
    pygame.quit()
    sys.exit()

def game_over_screen(surface, font, score, level):
    surface.fill(BLACK)
    display_text(surface, "GAME OVER", font, (200, 0, 0), SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 20)
    display_text(surface, f"Final Score: {score}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 10)
    display_text(surface, f"Level Reached: {level}", font, WHITE, SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40)
    pygame.display.update()
    pygame.time.delay(2000)

if __name__ == "__main__":
    main()
