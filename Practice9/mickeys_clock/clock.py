import math
import pygame


def draw_hand(screen, center, length, angle, color, width):
    radians = math.radians(angle - 90)
    end = (center[0] + int(math.cos(radians) * length),
           center[1] + int(math.sin(radians) * length))
    pygame.draw.line(screen, color, center, end, width)
    pygame.draw.circle(screen, (255, 255, 255), end, width)


def draw_clock(screen, center, radius, minute, second):
    draw_hand(screen, center, radius * 0.5, minute * 6, (30, 30, 30), 12)
    draw_hand(screen, center, radius * 0.7, second * 6, (220, 40, 50), 8)
    pygame.draw.circle(screen, (30, 30, 30), center, 12)
