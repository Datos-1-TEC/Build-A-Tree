import pygame
import time


displayWidth = 950
displayHeight = 700
width = 65
height = 60


pygame.init()

walkRight = [pygame.image.load("resources/megaman1.png"), pygame.image.load("resources/megaman2.png"), pygame.image.load("resources/megaman3.png"), pygame.image.load("resources/megaman4.png")]
walkLeft = [pygame.image.load("resources/megaman_1.png"), pygame.image.load("resources/megaman_2.png"), pygame.image.load("resources/megaman_3.png"), pygame.image.load("resources/megaman_4.png")]
playerOne = pygame.image.load("resources/megamanstand.png")
bg = pygame.image.load("resources/background.jpg")

window = pygame.display.set_mode((displayWidth,displayHeight))
displayFlag = True
isJump = False
x = 250
y = 250
vel = 10
jumpCount = 10
walkCount = 0
left = False
right = False

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0


    def draw(self, window):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if self.left:
            window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            window.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            window.blit(playerOne, (self.x, self.y))



megaman = player(300, 410, 65, 60)

def redrawGameWindow():
    global megaman
    window.blit(bg, (0, 0))
    megaman.draw(window)
    pygame.display.update()


pygame.display.set_caption("Build a Tree")
def main():
    global displayFlag, isJump, x, y, vel, jumpCount, clock, walkCount,left, right, megaman
        
    
    #window.blit(player, (100, 100))
    while displayFlag:
        clock.tick(12)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                displayFlag = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and megaman.x > megaman.vel:
            megaman.x -= megaman.vel
            megaman.left = True
            megaman.right = False
        elif keys[pygame.K_RIGHT] and megaman.x < 900 - megaman.width - megaman.vel:
            megaman.x += megaman.vel
            megaman.right = True
            megaman.left = False
        else:
            megaman.right = False
            megaman.left = False
            megaman.walkCount = 0

        if not(megaman.isJump):
            if keys[pygame.K_UP]:
                megaman.isJump = True
                megaman.right = False
                megaman.left = False
                megaman.walkCount = 0
        else:
            if megaman.jumpCount >= -10:
                negative = 1
                if megaman.jumpCount < 0:
                    negative = -1
                megaman.y -= (megaman.jumpCount ** 2) * 0.5 * negative
                megaman.jumpCount -= 1
            else:
                megaman.isJump = False
                megaman.jumpCount = 10

        redrawGameWindow()

    

main()
    







