import pygame

#Constants 
ALPHA = (0,255,0)


#class that creates a platform so the players can stand or fight in the game 

class Platform(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos, imgW,imgH,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/Pad_03_1.png").convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
