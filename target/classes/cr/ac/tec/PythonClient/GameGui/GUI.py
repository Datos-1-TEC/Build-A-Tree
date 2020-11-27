import pygame
import time


displayWidth = 950
displayHeight = 700
width = 65
height = 60


pygame.init()

#Player one
walkRight = [pygame.image.load("resources/megaman1.png"), pygame.image.load("resources/megaman2.png"), pygame.image.load("resources/megaman3.png"), pygame.image.load("resources/megaman4.png")]
walkLeft = [pygame.image.load("resources/megaman_1.png"), pygame.image.load("resources/megaman_2.png"), pygame.image.load("resources/megaman_3.png"), pygame.image.load("resources/megaman_4.png")]
playerOne = pygame.image.load("resources/megamanstand.png")

#Player two
walkRight2 = [pygame.image.load("resources/samus1.png"), pygame.image.load("resources/samus2.png"), pygame.image.load("resources/samus3.png"), pygame.image.load("resources/samus4.png"), pygame.image.load("resources/samus5.png"), pygame.image.load("resources/samus6.png"), pygame.image.load("resources/samus7.png"), pygame.image.load("resources/samus8.png"), pygame.image.load("resources/samus9.png"), pygame.image.load("resources/samus91.png")]
walkLeft2 = [pygame.image.load("resources/samus_1.png"), pygame.image.load("resources/samus_2.png"), pygame.image.load("resources/samus_3.png"), pygame.image.load("resources/samus_4.png"), pygame.image.load("resources/samus_5.png"), pygame.image.load("resources/samus_6.png"), pygame.image.load("resources/samus_7.png"), pygame.image.load("resources/samus_8.png"), pygame.image.load("resources/samus_9.png"), pygame.image.load("resources/samus_91.png")]
playerTwo = 

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
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 32, 52)


    def draw(self, window):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 32, 52)
        pygame.draw.rect(window, (255, 0, 0), (self.hitbox), 2)


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing #se encarga de direccionar la bala dependiendo de a donde se estaba moviendo
        self.vel = 30 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)





megaman = player(300, 410, 65, 60)
bullets = []

def redrawGameWindow():
    global megaman, bullets
    window.blit(bg, (0, 0))
    megaman.draw(window)
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


pygame.display.set_caption("Build a Tree")
def main():
    global displayFlag, isJump, x, y, vel, jumpCount, clock, walkCount,left, right, megaman, bullets
        
    
    #window.blit(player, (100, 100))
    while displayFlag:
        clock.tick(12)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                displayFlag = False

        for bullet in bullets:
            if bullet.x < 950 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if megaman.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 10:
                bullets.append(projectile(round(megaman.x + megaman.width //2), round(megaman.y + megaman.height//2), 6, (0,0,0), facing))

        if keys[pygame.K_LEFT] and megaman.x > megaman.vel:
            megaman.x -= megaman.vel
            megaman.left = True
            megaman.right = False
            megaman.standing = False
        elif keys[pygame.K_RIGHT] and megaman.x < 900 - megaman.width - megaman.vel:
            megaman.x += megaman.vel
            megaman.right = True
            megaman.left = False
            megaman.standing = False
        else:
            megaman.standing = True
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
    







