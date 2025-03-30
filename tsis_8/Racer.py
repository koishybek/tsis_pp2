import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

player = pygame.Rect(200, 500, 40, 60)
coins = []
coin_timer = 0
coin_count = 0

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

    coin_timer += 1
    if coin_timer > 30:
        coins.append(pygame.Rect(random.randint(0, 360), 0, 20, 20))
        coin_timer = 0

    for coin in coins[:]:
        coin.move_ip(0, 5)
        if coin.colliderect(player):
            coins.remove(coin)
            coin_count += 1
        elif coin.top > 600:
            coins.remove(coin)

    pygame.draw.rect(screen, WHITE, player)
    for coin in coins:
        pygame.draw.ellipse(screen, YELLOW, coin)

    text = font.render(f"Coins: {coin_count}", True, WHITE)
    screen.blit(text, (250, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()