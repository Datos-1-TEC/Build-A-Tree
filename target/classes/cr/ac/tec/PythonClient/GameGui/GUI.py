import pygame
import time


displayWidth = 750
displayHeight = 600
width = 40
height = 60




pygame.init()
"""
white = (255, 255, 255)
player = pygame.image.load("resources/megaman1.png")
"""


pygame.display.set_caption("Build a Tree")
def main():
    displayFlag = True
    isJump = False
    x = 50
    y = 50
    vel = 15
    jumpCount = 10   
    window = pygame.display.set_mode((displayWidth,displayHeight))
    
    #window.blit(player, (100, 100))
    while displayFlag:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
            if jumpCount >= -10:
                negative = 1
                if jumpCount < 0:
                    negative = -1
                y -= (jumpCount ** 2) * 0.5 * negative
                jumpCount -= 1
            else:
                isJump = False
                jumpCount = 10

        window.fill((0,0,0))

        player = pygame.image.load("resources/megaman1.png").convert_alpha()
        rect = player.get_rect()
        rect.center = (200, 300)
        rect.move(x, y)
        window.blit(player, rect)



        pygame.display.update()
    
    

    


main()
    






