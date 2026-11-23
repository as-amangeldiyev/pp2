from datetime import datetime
from pathlib import Path

import pygame

from tools import draw_shape, flood_fill


pygame.init()
pygame.display.set_caption("TSIS 2 Paint")
screen = pygame.display.set_mode((1000, 700))
canvas = pygame.Surface((1000, 580))
canvas.fill("white")
font = pygame.font.SysFont(None, 22)
large_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

toolbar_height = 120
tools = ["pencil", "line", "rectangle", "circle", "eraser", "fill",
         "square", "right triangle", "triangle", "rhombus", "text"]
colors = [(20, 20, 20), (220, 45, 45), (40, 100, 220), (30, 160, 80),
          (245, 190, 35), (150, 70, 190), (255, 255, 255), (110, 110, 110)]
tool_rects = []
for number, name in enumerate(tools):
    row, column = divmod(number, 6)
    tool_rects.append((name, pygame.Rect(12 + column * 160, 56 + row * 30, 150, 26)))
color_rects = []
for number, color in enumerate(colors):
    rect = pygame.Rect(15 + number * 34, 12, 26, 26)
    color_rects.append((color, rect))

tool = "pencil"
color = colors[0]
brush_sizes = [2, 5, 10]
brush_index = 1
brush_size = brush_sizes[brush_index]
start = None
last = None
drawing = False
text_position = None
text_input = ""
running = True


def canvas_position(point):
    return point[0], point[1] - toolbar_height


def save_canvas():
    output = Path(__file__).parent / "saves"
    output.mkdir(exist_ok=True)
    filename = datetime.now().strftime("canvas_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, output / filename)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if text_position is not None:
                    rendered = font.render(text_input, True, color, "white")
                    canvas.blit(rendered, text_position)
                    text_position = None
                    text_input = ""
                    pygame.key.stop_text_input()
                save_canvas()
            elif text_position is not None:
                if event.key == pygame.K_RETURN:
                    rendered = font.render(text_input, True, color, "white")
                    canvas.blit(rendered, text_position)
                    text_position = None
                    text_input = ""
                    pygame.key.stop_text_input()
                elif event.key == pygame.K_ESCAPE:
                    text_position = None
                    text_input = ""
                    pygame.key.stop_text_input()
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                brush_index = event.key - pygame.K_1
                brush_size = brush_sizes[brush_index]
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.TEXTINPUT and text_position is not None:
            text_input += event.text
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if y < toolbar_height:
                for name, rect in tool_rects:
                    if rect.collidepoint(event.pos):
                        tool = name
                for selected_color, rect in color_rects:
                    if rect.collidepoint(event.pos):
                        color = selected_color
            else:
                position = canvas_position(event.pos)
                if tool == "fill":
                    flood_fill(canvas, position, color)
                elif tool == "text":
                    text_position = position
                    text_input = ""
                    pygame.key.start_text_input()
                else:
                    start = position
                    last = position
                    drawing = True
                    if tool in ("pencil", "eraser"):
                        stroke_color = "white" if tool == "eraser" else color
                        pygame.draw.circle(canvas, stroke_color, position, max(1, brush_size // 2))
        elif event.type == pygame.MOUSEMOTION and drawing:
            position = canvas_position(event.pos)
            if 0 <= position[0] < canvas.get_width() and 0 <= position[1] < canvas.get_height():
                if tool in ("pencil", "eraser"):
                    stroke_color = "white" if tool == "eraser" else color
                    pygame.draw.line(canvas, stroke_color, last, position, brush_size)
                    last = position
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            position = canvas_position(event.pos)
            position = (max(0, min(canvas.get_width() - 1, position[0])),
                        max(0, min(canvas.get_height() - 1, position[1])))
            if tool not in ("pencil", "eraser"):
                draw_shape(canvas, tool, start, position, color, brush_size)
            drawing = False

    screen.fill((225, 228, 235))
    pygame.draw.rect(screen, (245, 246, 249), (0, 0, 1000, toolbar_height))
    for selected_color, rect in color_rects:
        pygame.draw.rect(screen, selected_color, rect)
        pygame.draw.rect(screen, (40, 40, 45), rect, 1)
    for name, rect in tool_rects:
        fill_color = (195, 210, 240) if name == tool else (230, 232, 237)
        pygame.draw.rect(screen, fill_color, rect, border_radius=4)
        screen.blit(font.render(name, True, (30, 32, 38)), (rect.x + 7, rect.y + 5))
    screen.blit(font.render(f"Brush: {brush_size}px   Keys 1 / 2 / 3", True, (35, 37, 43)), (310, 14))
    screen.blit(canvas, (0, toolbar_height))

    if drawing and tool not in ("pencil", "eraser"):
        preview = canvas.copy()
        position = canvas_position(pygame.mouse.get_pos())
        position = (max(0, min(canvas.get_width() - 1, position[0])),
                    max(0, min(canvas.get_height() - 1, position[1])))
        draw_shape(preview, tool, start, position, color, brush_size)
        screen.blit(preview, (0, toolbar_height))
    if text_position is not None:
        text_surface = font.render(text_input, True, color, "white")
        screen.blit(text_surface, (text_position[0], text_position[1] + toolbar_height))
        pygame.draw.line(screen, color,
                         (text_position[0], text_position[1] + toolbar_height),
                         (text_position[0], text_position[1] + toolbar_height + font.get_height()), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
