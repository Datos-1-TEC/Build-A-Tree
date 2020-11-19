import pygame
import time


pygame.init()

displayWidth = 750
displayHeight = 600
x = 50
y= 50
width = 40
height = 60
vel = 5
isJump = False
jumpCount = 10

window = pygame.display.set_mode((displayWidth,displayHeight))

pygame.display.set_caption("Build a Tree")

displayFlag = True
while displayFlag:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            displayFlag = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < 750 - width - vel:
        x += vel
    if not(isJump):
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < 500 - height - vel:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCOunt >= -10:
            negative = 1
            if jumpCount < 0:
                negative = -1
            y -= (jumpCount ** 2) * 0.5 * negative
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    



pygame.quit()



