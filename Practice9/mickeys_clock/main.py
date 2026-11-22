from datetime import datetime
from pathlib import Path

import pygame

from clock import draw_clock


pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Mickey's Clock")
image_path = Path(__file__).parent / "images" / "mickeyclock.jpeg"
image = pygame.transform.smoothscale(pygame.image.load(str(image_path)), (620, 465))
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()
center = (450, 330)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False

    now = datetime.now()
    screen.fill((25, 27, 36))
    screen.blit(image, image.get_rect(center=center))
    draw_clock(screen, center, 180, now.minute, now.second)
    time_text = font.render(now.strftime("%M:%S"), True, (255, 255, 255))
    screen.blit(time_text, time_text.get_rect(center=(450, 625)))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
