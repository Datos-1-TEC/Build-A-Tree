import pygame
import sys
from pygame.locals import *

listNodes = []
class Node:
    def __init__(self, data, x, y):
        self.left = None
        self.right = None
        self.data = data
        self.x = x
        self.y = y

# Insert method to create nodes

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def getData(self):
        return self.data

    def insert(self, data, x, y):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data, x, y)
                    listNodes.append(self.left)
                else:
                    self.left.insert(data,  x, y)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data, x, y)
                    listNodes.append(self.right)
                else:
                    self.right.insert(data, x, y)
        else:
            self.data = data
# findval method to compare the value with nodes
    def findval(self, lkpval):
        if lkpval < self.data:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.findval(lkpval)
        elif lkpval > self.data:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.findval(lkpval)
        else:
            return self.data
# Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()




white = (255,255,255)
black = (0,0,0)


class Pane(object):
    def __init__(self):
        self.root = Node(12, 100, 10)
        self.root.insert(6, 100, 110)
        self.root.insert(14,  100, 210)
        self.root.insert(3,  100, 310)
        print(listNodes[0].getY())
        print(listNodes[1].getY())
        print(listNodes[2].getY())
        
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 12)
        pygame.display.set_caption("Trees")
        self.screen = pygame.display.set_mode((600,400), 0, 32)
        self.screen.fill((white))
        pygame.display.update()
        self.posX = 0
        self.posY = 0


    def addRect(self):
        self.posX = self.root.getX()
        self.posY = self.root.getY()
        self.posX1 = listNodes[0].getX()
        self.posY1 = listNodes[0].getY()
        self.posX2 = listNodes[1].getX()
        self.posY2 = listNodes[1].getY()
        self.rect = pygame.draw.rect(self.screen, (black), (self.posX, self.posY, 25, 25), 2)
        self.rect1 = pygame.draw.rect(self.screen, (black), (self.posX1 , self.posY1 , 25, 25), 2)
        self.rect2 = pygame.draw.rect(self.screen, (black), (self.posX2 , self.posY2 , 25, 25), 2)

        pygame.display.update()

    def addText(self):
        value = str(self.root.getData())
        value1 = str(listNodes[0].getData())
        value2 = str(listNodes[1].getData())
        self.screen.blit(self.font.render(value, True, (255,0,0)), (self.posX+5, self.posY +5))
        self.screen.blit(self.font.render(value1, True, (255,0,0)), (self.posX1 + 5, self.posY1 + 5))
        self.screen.blit(self.font.render(value2, True, (255,0,0)), (self.posX2 +5 , self.posY2 + 5))
        pygame.display.update()

if __name__ == '__main__':
    Pan3 = Pane()
    Pan3.addRect()
    Pan3.addText()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();