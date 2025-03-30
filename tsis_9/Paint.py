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

# Игровой цикл
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
            x1, y1 = start_pos
            x2, y2 = end_pos
            if mode == 'draw':
                pygame.draw.line(screen, color, start_pos, end_pos, 3)
            elif mode == 'rect':
                pygame.draw.rect(screen, color, pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), 3)
            elif mode == 'square':
                size = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, pygame.Rect(x1, y1, size, size), 3)
            elif mode == 'circle':
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 3)
            elif mode == 'eraser':
                pygame.draw.line(screen, WHITE, start_pos, end_pos, 10)
            elif mode == 'triangle':
                pygame.draw.polygon(screen, color, [(x1, y2), ((x1 + x2) // 2, y1), (x2, y2)], 3)
            elif mode == 'right_triangle':
                pygame.draw.polygon(screen, color, [start_pos, (x1, y2), (x2, y2)], 3)
            elif mode == 'rhombus':
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                points = [(center[0], center[1] - dy), (center[0] + dx, center[1]), (center[0], center[1] + dy), (center[0] - dx, center[1])]
                pygame.draw.polygon(screen, color, points, 3)
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
            elif event.key == pygame.K_s:
                mode = 'square'
            elif event.key == pygame.K_t:
                mode = 'triangle'
            elif event.key == pygame.K_h:
                mode = 'right_triangle'
            elif event.key == pygame.K_m:
                mode = 'rhombus'
            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = BLUE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
