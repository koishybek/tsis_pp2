import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint Program")

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
GREEN = (0,   255, 0)
BLUE  = (0,   0,   255)
YELLOW= (255, 255, 0)

# A small palette of colors to choose from
color_palette = [BLACK, RED, GREEN, BLUE, YELLOW]
current_color = BLACK  # Default drawing color

background_color = WHITE

# Added new tools for shapes
tools = [
    "pencil",
    "rectangle",
    "circle",
    "eraser",
    "square",
    "triangle_right",
    "triangle_equilateral",
    "rhombus"
]

# Use more descriptive labels for tools (instead of just t[0])
tool_labels = {
    "pencil":              "P",
    "rectangle":           "R",
    "circle":              "C",
    "eraser":              "E",
    "square":              "S",
    "triangle_right":      "Tr",
    "triangle_equilateral":"Te",
    "rhombus":             "Rh"
}

current_tool = "pencil"
eraser_radius = 10

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(background_color)

# For real-time drawing of shapes while dragging
preview = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
preview = preview.convert_alpha()
preview.fill((0, 0, 0, 0))  # Transparent

drawing = False      # True when the mouse is held down
start_pos = (0, 0)   # Where the drag started (for shapes)
end_pos = (0, 0)     # Current mouse position (for shapes)

clock = pygame.time.Clock()

def draw_pencil(pos, color):
    """Draw a small circle (like a pencil tip) on the canvas."""
    pygame.draw.circle(canvas, color, pos, 2)

def draw_eraser(pos, radius):
    """Erase by drawing a circle in the background color."""
    pygame.draw.circle(canvas, background_color, pos, radius)

def draw_rectangle(surface, color, start, end):
    """Draw a rectangle from start to end on the given surface."""
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    rect = pygame.Rect(min(x1, x2), min(y1, y2), width, height)
    pygame.draw.rect(surface, color, rect, 1)

def draw_circle(surface, color, start, end):
    """Draw a circle on the given surface based on start-end drag."""
    x1, y1 = start
    x2, y2 = end
    radius = int(math.hypot(x2 - x1, y2 - y1))
    pygame.draw.circle(surface, color, start, radius, 1)

def draw_square(surface, color, start, end):
    """
    Draw a square.  
    The square's side = min(width, height) of the bounding box.
    """
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    side = min(width, height)
    left = min(x1, x2)
    top = min(y1, y2)
    rect = pygame.Rect(left, top, side, side)
    pygame.draw.rect(surface, color, rect, 1)

def draw_triangle_right(surface, color, start, end):
    """
    Draw a right triangle using the bounding box formed by start and end.  
    We'll make the top-left corner, top-right corner, and bottom-left corner
    be the triangle's three points.
    """
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    # Right triangle points (top-left, top-right, bottom-left)
    points = [
        (left, top),
        (right, top),
        (left, bottom)
    ]
    pygame.draw.polygon(surface, color, points, 1)

def draw_triangle_equilateral(surface, color, start, end):
    """
    Draw an equilateral triangle roughly within the bounding box.  
    - We'll define the base along the bottom of the bounding box.
    - Side length = min(width, height)
    - The apex is centered horizontally above the base.
    """
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    
    side = min(right - left, bottom - top)  # side length to fit bounding box
    # base points
    p1 = (left,  bottom)
    p2 = (left + side, bottom)
    # apex (centered horizontally above base)
    apex_x = left + side / 2
    # height of equilateral triangle
    height = (math.sqrt(3) / 2) * side
    apex_y = bottom - height
    p3 = (apex_x, apex_y)

    points = [p1, p2, p3]
    pygame.draw.polygon(surface, color, points, 1)

def draw_rhombus(surface, color, start, end):
    """
    Draw a rhombus (diamond shape) using the bounding box.  
    The diagonals of the bounding box become the diagonals of the rhombus.
    """
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    
    cx = (left + right) / 2
    cy = (top + bottom) / 2
    
    # Diamond corners
    p1 = (cx, top)       # top
    p2 = (right, cy)     # right
    p3 = (cx, bottom)    # bottom
    p4 = (left, cy)      # left
    
    points = [p1, p2, p3, p4]
    pygame.draw.polygon(surface, color, points, 1)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if user clicked on color palette
            for i, c in enumerate(color_palette):
                palette_rect = pygame.Rect(10 + 50 * i, 10, 40, 40)
                if palette_rect.collidepoint(mouse_x, mouse_y):
                    current_color = c

            # Check if user clicked on a tool
            for i, t in enumerate(tools):
                tool_rect = pygame.Rect(10 + 50*i, 60, 40, 40)
                if tool_rect.collidepoint(mouse_x, mouse_y):
                    current_tool = t

            drawing = True
            start_pos = event.pos
            end_pos = event.pos

            # If the user starts drawing immediately with pencil/eraser
            if current_tool == "pencil":
                draw_pencil(event.pos, current_color)
            elif current_tool == "eraser":
                draw_eraser(event.pos, eraser_radius)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False
                # Finalize shape onto the canvas
                if current_tool == "rectangle":
                    draw_rectangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos)
                elif current_tool == "triangle_right":
                    draw_triangle_right(canvas, current_color, start_pos, end_pos)
                elif current_tool == "triangle_equilateral":
                    draw_triangle_equilateral(canvas, current_color, start_pos, end_pos)
                elif current_tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)

            # Clear preview after finalizing
            preview.fill((0, 0, 0, 0))

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos
                if current_tool == "pencil":
                    draw_pencil(end_pos, current_color)
                elif current_tool == "eraser":
                    draw_eraser(end_pos, eraser_radius)
                else:
                    # For shape tools, draw on the preview
                    preview.fill((0, 0, 0, 0))
                    if current_tool == "rectangle":
                        draw_rectangle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "circle":
                        draw_circle(preview, current_color, start_pos, end_pos)
                    elif current_tool == "square":
                        draw_square(preview, current_color, start_pos, end_pos)
                    elif current_tool == "triangle_right":
                        draw_triangle_right(preview, current_color, start_pos, end_pos)
                    elif current_tool == "triangle_equilateral":
                        draw_triangle_equilateral(preview, current_color, start_pos, end_pos)
                    elif current_tool == "rhombus":
                        draw_rhombus(preview, current_color, start_pos, end_pos)

    # Draw the canvas and the preview
    screen.blit(canvas, (0, 0))
    screen.blit(preview, (0, 0))

    # Draw color palette (with highlight if selected)
    for i, c in enumerate(color_palette):
        palette_rect = pygame.Rect(10 + 50*i, 10, 40, 40)
        pygame.draw.rect(screen, c, palette_rect)
        if c == current_color:
            pygame.draw.rect(screen, BLACK, palette_rect, 2)

    # Draw tool buttons
    for i, t in enumerate(tools):
        tool_rect = pygame.Rect(10 + 50*i, 60, 40, 40)
        pygame.draw.rect(screen, (200, 200, 200), tool_rect)
        font = pygame.font.SysFont(None, 22)
        # Use the dictionary to get a more descriptive label
        label_text = tool_labels[t]
        txt = font.render(label_text, True, BLACK)
        txt_rect = txt.get_rect(center=tool_rect.center)
        screen.blit(txt, txt_rect)

        if t == current_tool:
            pygame.draw.rect(screen, BLACK, tool_rect, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
