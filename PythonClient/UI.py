import pygame
pygame.init()

window = pygame.display.set_mode((500, 500))

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()