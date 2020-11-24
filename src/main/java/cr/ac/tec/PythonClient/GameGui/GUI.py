import pygame
import time


walkRight = [pygame.image.load("resources/megaman1.png"), pygame.image.load("resources/megaman2.png"), pygame.image.load("resources/megaman3.png"), pygame.image.load("resources/megaman4.png")]
walkLeft = [pygame.image.load("resources/megaman_1.png"), pygame.image.load("resources/megaman_2.png"), pygame.image.load("resources/megaman_3.png"), pygame.image.load("resources/megaman_4.png")]
playerOne = pygame.image.load("resources/megamanstand.png")
bg = pygame.image.load("resources/background.jpg")

displayWidth = 950
displayHeight = 700
width = 40
height = 60
left = False
right = False
walkCount = 0


pygame.init()

window = pygame.display.set_mode((displayWidth,displayHeight))
displayFlag = True
isJump = False
x = 250
y = 250
vel = 15
jumpCount = 10

clock = pygame.time.Clock()


def redrawGameWindow():
    global walkCount
    window.blit(bg, (0, 0))

    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        window.blit(walkLeft[walkCount//3], (x, y))
        walkCount += 1
    elif right:
        window.blit(walkRight[walkCount//3], (x, y))
        walkCount += 1
    else:
        window.blit(playerOne, (x, y))

    pygame.display.update()


pygame.display.set_caption("Build a Tree")
def main():
    global displayFlag, isJump, x, y, vel, jumpCount, clock
     
    
    #window.blit(player, (100, 100))
    while displayFlag:
        clock.tick(27)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                displayFlag = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > vel:
            x -= vel
            left = True
            right = False
        elif keys[pygame.K_RIGHT] and x < 900 - width - vel:
            x += vel
            right = True
            left = False
        else:
            right = False
            left = False
            walkCount = 0

        if not(isJump):
            if keys[pygame.K_SPACE]:
                isJump = True
                right = False
                left = False
                walkCount = 0
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

        redrawGameWindow()

    
    

    


main()
    







