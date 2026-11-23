from collections import deque
import math

import pygame


def draw_shape(surface, tool, start, end, color, size):
    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)
    elif tool == "rectangle":
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1).normalize()
        pygame.draw.rect(surface, color, rect, size)
    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start, radius, size)
    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        x2 = x1 + side * (1 if x2 >= x1 else -1)
        y2 = y1 + side * (1 if y2 >= y1 else -1)
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1).normalize()
        pygame.draw.rect(surface, color, rect, size)
    elif tool == "right triangle":
        pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x1, y2)], size)
    elif tool == "triangle":
        middle = ((x1 + x2) // 2, (y1 + y2) // 2)
        dx, dy = x2 - x1, y2 - y1
        height = math.sqrt(3) / 2
        tip = (round(middle[0] - dy * height), round(middle[1] + dx * height))
        pygame.draw.polygon(surface, color, [start, end, tip], size)
    elif tool == "rhombus":
        middle = ((x1 + x2) // 2, (y1 + y2) // 2)
        dx, dy = x2 - x1, y2 - y1
        points = [start, (middle[0] + dy // 2, middle[1] - dx // 2), end,
                  (middle[0] - dy // 2, middle[1] + dx // 2)]
        pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, position, color):
    width, height = surface.get_size()
    x, y = position
    target = surface.get_at((x, y))
    replacement = (*color, 255)
    if target == replacement:
        return

    pending = deque([position])
    visited = {position}
    while pending:
        x, y = pending.popleft()
        if surface.get_at((x, y)) != target:
            continue
        surface.set_at((x, y), color)
        for point in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            px, py = point
            if 0 <= px < width and 0 <= py < height and point not in visited:
                visited.add(point)
                pending.append(point)
