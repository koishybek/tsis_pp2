import pygame
import sys
import time
import os
import math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame App")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

mickey = pygame.image.load('mickeyclock.jpeg')
mickey = pygame.transform.scale(mickey, (300, 300))
mickey_rect = mickey.get_rect(center=(WIDTH // 2, HEIGHT // 2))

ball_pos = [WIDTH // 2, HEIGHT // 2]
BALL_RADIUS = 25
BALL_SPEED = 20

MUSIC_FOLDER = r"C:\Users\koish\OneDrive\Рабочий стол\tsis_file\tsis\tsis_7"
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]
current_track = 0

if music_files:
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_track]))


def draw_clock():
    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    screen.blit(mickey, mickey_rect.topleft)

    minute_angle = -minutes * 6 + 90
    second_angle = -seconds * 6 + 90

    minute_length = 60
    second_length = 80

    minute_x = WIDTH // 2 + math.cos(math.radians(minute_angle)) * minute_length
    minute_y = HEIGHT // 2 - math.sin(math.radians(minute_angle)) * minute_length
    second_x = WIDTH // 2 + math.cos(math.radians(second_angle)) * second_length
    second_y = HEIGHT // 2 - math.sin(math.radians(second_angle)) * second_length

    pygame.draw.line(screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), (minute_x, minute_y), 4)
    pygame.draw.line(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2), (second_x, second_y), 2)


def draw_ball():
    pygame.draw.circle(screen, RED, ball_pos, BALL_RADIUS)


def move_ball(keys):
    if keys[pygame.K_UP] and ball_pos[1] - BALL_RADIUS > 0:
        ball_pos[1] -= BALL_SPEED
    if keys[pygame.K_DOWN] and ball_pos[1] + BALL_RADIUS < HEIGHT:
        ball_pos[1] += BALL_SPEED
    if keys[pygame.K_LEFT] and ball_pos[0] - BALL_RADIUS > 0:
        ball_pos[0] -= BALL_SPEED
    if keys[pygame.K_RIGHT] and ball_pos[0] + BALL_RADIUS < WIDTH:
        ball_pos[0] += BALL_SPEED


def handle_music(keys):
    global current_track
    if keys[pygame.K_SPACE]:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    if keys[pygame.K_s]:
        pygame.mixer.music.stop()

    if keys[pygame.K_n]:
        current_track = (current_track + 1) % len(music_files)
        pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_track]))
        pygame.mixer.music.play()

    if keys[pygame.K_p]:
        current_track = (current_track - 1) % len(music_files)
        pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_track]))
        pygame.mixer.music.play()


def main():
    running = True
    if music_files:
        pygame.mixer.music.play()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        move_ball(keys)
        handle_music(keys)
        draw_clock()
        draw_ball()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
