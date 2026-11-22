import pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()
x, y = 400, 300
radius = 25
step = 20
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_UP and y - step >= radius:
                y -= step
            elif event.key == pygame.K_DOWN and y + step <= 600 - radius:
                y += step
            elif event.key == pygame.K_LEFT and x - step >= radius:
                x -= step
            elif event.key == pygame.K_RIGHT and x + step <= 800 - radius:
                x += step

    screen.fill("white")
    pygame.draw.circle(screen, "red", (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
