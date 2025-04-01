# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing 
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Movement speeds
SPEED = 5         # Controls how fast coins (and anything else using SPEED) fall
ENEMY_SPEED = 5   # Controls how fast the enemy moves down the screen

# Scoring and coin variables
SCORE = 0
COINS_COLLECTED = 0

# Fonts and images
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Use ENEMY_SPEED instead of SPEED, so enemy speed can be changed separately
        global SCORE
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Random weight for each coin
        self.weight = random.choice([1, 2, 3])  
        coin_img = pygame.image.load("coin.png")
        coin_img = pygame.transform.scale(coin_img, (25, 25))
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Coins move down the screen using the global SPEED
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Initialize Player and Enemy
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Timers for increasing speed and spawning coins
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Increase SPEED by 0.5 every second

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 2000) # Spawn a coin every 2 seconds

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))

    # Display SCORE in top-left
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Display collected coins in top-right
    coins_text = font_small.render(str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 30, 10))

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check for collision with Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill() 

        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check for collision with Coins
    coin_collisions = pygame.sprite.spritecollide(P1, coins, True)
    if coin_collisions:
        # Add up the total weight of all collected coins in this frame
        COINS_COLLECTED += sum(coin.weight for coin in coin_collisions)

        # Increase enemy speed after N coins collected (example threshold: 10)
        if COINS_COLLECTED >= 10:
            ENEMY_SPEED = 8   # Adjust as needed

    pygame.display.update()
    FramePerSec.tick(FPS)
