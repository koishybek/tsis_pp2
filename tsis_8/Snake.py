import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

snake = [(20, 20)]
direction = (20, 0)
food = (100, 100)
speed = 10
score = 0
level = 1

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 20):
        direction = (0, -20)
    if keys[pygame.K_DOWN] and direction != (0, -20):
        direction = (0, 20)
    if keys[pygame.K_LEFT] and direction != (20, 0):
        direction = (-20, 0)
    if keys[pygame.K_RIGHT] and direction != (-20, 0):
        direction = (20, 0)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400 or new_head in snake:
        running = False

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        while True:
            food = (random.randint(0, 19)*20, random.randint(0, 19)*20)
            if food not in snake:
                break
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    for s in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(s[0], s[1], 20, 20))
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], 20, 20))

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()