from graphics import *
from BTree import *
from AVLTree import *
import random


class drawnTree:        
        
        def drawTree(self, tree):
                			
                tree.markOrder()
                if (tree.rootNode != None):                     
                        
                        for x in range(0,tree.numNodes):
                                p1 = Point(x*self.cellSize,0)
                                p2 = Point((x+1)*self.cellSize, (self.h+1)*self.cellSize)
                                rect = Rectangle(p1,p2)
                                rect.setFill(color_rgb(250 - (x%2)*5,240 - (x%2)*5, 245 - (x%2)*5))
                                rect.draw(self.win)
                                
                        c = tree.getFirst()		
                        while (c != None):
                                if (c.parent != None):
                                        p1 = Point(c.order*self.cellSize+self.halfCellSize, (c.depth*self.cellSize+self.halfCellSize))
                                        p2 = Point(c.parent.order*self.cellSize+self.halfCellSize, (c.parent.depth*self.cellSize+self.halfCellSize))
                                        lin = Line(p1,p2)
                                        lin.draw(self.win)
                                c = c.next()
                        
                        c = tree.getFirst()
                        column = 0
                        while (c != None):
                                p = Point(column*self.cellSize+self.halfCellSize, (c.depth*self.cellSize+self.halfCellSize))
                                circ = Circle(p, self.nodeSize)
                                circ2 = Circle(p, self.nodeSize-5)
                                txt = Text(p, c.keyData)
                                
                                if (c == tree.currentNode):
                                        circ.setFill(color_rgb(0,255,0))
                                elif (tree.currentNode != None):
                                        if (c == tree.currentNode.next()):
                                                circ.setFill(color_rgb(0,0,255))
                                        elif (c == tree.currentNode.prev()):
                                                circ.setFill(color_rgb(255,0,0))
                                        else:
                                                circ.setFill(color_rgb(0,0,0))
                                else:
                                        circ.setFill(color_rgb(0,0,0))
                                        
                                circ2.setFill(color_rgb(255,255,255))
                                circ.draw(self.win)
                                circ2.draw(self.win)
                                txt.draw(self.win)
                                c = c.next()
                                column += 1

        def update(self, a):
                self.tree = a
                self.h = a.rootNode.height
                self.w = a.numNodes
                self.win.width = a.numNodes
                self.win.height = a.rootNode.height
                self.win.flush()
                self.win.redraw()
                #self.win.setCoords(0,0,self.w,self.h)
                #self.win.master.geometry("150x1000")
                self.drawTree(a)
                

        def myfunc(self):
                self.drawTree(self.tree)
                
        def __init__(self, T, wT):
                print("estoy en el init")
                print(__name__)
                self.tree = T
                self.title = wT
                self.cellSize = 50
                self.nodeSize = 24
                self.halfCellSize = self.cellSize / 2
                self.h = T.rootNode.height
                self.w = T.numNodes		
                self.win = GraphWin(self.title, 960, 540)
                #drawTree(self.tree, self.title)

        #if __name__ == "drawTree":
         #       print("estoy en el main")
        #        drawTree(self.tree, self.title)
                            
                        #input("Press Enter to continue...")
                        #win.close()
