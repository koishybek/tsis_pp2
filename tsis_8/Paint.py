import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen.fill(WHITE)
color = BLACK
mode = 'draw'
drawing = False
start_pos = (0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            if mode == 'draw':
                pygame.draw.line(screen, color, start_pos, end_pos, 3)
            elif mode == 'rect':
                rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                pygame.draw.rect(screen, color, rect, 3)
            elif mode == 'circle':
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 3)
            elif mode == 'eraser':
                pygame.draw.line(screen, WHITE, start_pos, end_pos, 10)
            drawing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 'rect'
            elif event.key == pygame.K_c:
                mode = 'circle'
            elif event.key == pygame.K_d:
                mode = 'draw'
            elif event.key == pygame.K_e:
                mode = 'eraser'
            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = BLUE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
