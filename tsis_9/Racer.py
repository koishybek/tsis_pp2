import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

player = pygame.Rect(200, 500, 40, 60)
coins = []
coin_timer = 0
coin_count = 0
coin_threshold = 5

enemy = pygame.Rect(200, 0, 40, 60)
enemy_speed = 5

# Игровой цикл
running = True
while running:
    screen.fill(GRAY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < 400:
        player.move_ip(5, 0)

    # Генерация монет
    coin_timer += 1
    if coin_timer > 30:
        weight = random.choice([1, 2, 3])
        coins.append({"rect": pygame.Rect(random.randint(0, 360), 0, 20, 20), "weight": weight})
        coin_timer = 0

    # Обработка монет
    for coin in coins[:]:
        coin["rect"].move_ip(0, 5)
        if coin["rect"].colliderect(player):
            coin_count += coin["weight"]
            coins.remove(coin)
        elif coin["rect"].top > 600:
            coins.remove(coin)

    # Увеличение скорости врага при достижении порога
    if coin_count >= coin_threshold:
        enemy_speed += 1
        coin_threshold += 5

    # Отрисовка
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, RED, enemy)
    enemy.move_ip(0, enemy_speed)
    if enemy.top > 600:
        enemy.top = 0
        enemy.left = random.randint(0, 360)

    for coin in coins:
        pygame.draw.ellipse(screen, YELLOW, coin["rect"])

    text = font.render(f"Coins: {coin_count}", True, WHITE)
    screen.blit(text, (250, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()