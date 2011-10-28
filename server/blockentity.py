# -*- coding: utf-8 -*-
import pygame 
from defines import *
from entity import Entity

"""
Generic class for all projectiles in the game.

"""
class BlockEntity(Entity):
    #def __init__(self, (x,y), vel, rot, filename, size, parent):
    def __init__(self, (x,y), vel, rot, (r,g,b), size, parent):
        Entity.__init__(self, (x, y), size / 2)
        self.color = (r,g,b)
        self.x = x
        self.y = y
        self.collide_rect = x,y
        self.walkable = 1
        self.size = size
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = 0 
        self.adjacentList = []
        if self.color == [000,000,000]:
            self.walkable = 0


    def getRect(self):
        return (x, y, BLOCKSIZE, BLOCKSIZE)
    def isWalkable(self):
        if self.color == black:
            return 0
        return 1
    def toString(self):
        return str(self.x) + " " + str(self.y)+ " " + str(self.color) + " " + str(self.size) + "\n"
    def setColor(self,color):
        self.color = color
        

    def drawFGH(self,screen):
        self.font = pygame.font.Font(None,12)
        self.fpsString = "F: " + str(self.g) + "\nG:" + str(self.g) + "\nH:" + str(self.h)
        text = self.font.render(self.fpsString,True, black, (159,182,205))
        self.fpsRect = text.get_rect()
        self.fpsRect.centerx = self.x#self.screen.get_rect().centerx
        self.fpsRect.centery = self.y#self.screen.get_rect().centery
        screen.blit(text,self.fpsRect)
        pygame.display.update()
   
           
               
    def draw(self,screen):
        #change color if we got a val
        #if self.f != 0 and self.color != pink:
         #   self.setColor(blue)
        pygame.draw.rect(screen,self.color,(( self.x, self.y), (self.size-2,self.size-2)))
        
       # if self.color == pink and self.parent != 0:
       #     self.drawParentLine(screen)
        #if self.color == black:
        #    self.drawAdjacentLines(screen)
    def drawParentLine(self,screen):
        pygame.draw.line(screen, green, (self.x(self.size/2), self.y+(self.size/2)), (self.parent.getX()+(self.size/2), self.parent.getY()+(self.size/2)),1) 
    def drawAdjacentLines(self,screen):
        for adjacent in self.adjacentList:
            pygame.draw.line(screen, pink, (self.x+(self.size/2), self.y+(self.size/2)), (adjacent.getX()+(self.size/2),adjacent.getY()+(self.size/2)), 1)
            pygame.display.flip()

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getH(self):
        return self.h
    def getF(self):
        return self.f
    def getG(self):
        return self.g
    def getParent(self):
        return self.parent
    
    def getAdjacentList(self):
        return self.adjacentList
    
    def setAdjacentList(self, adjacentList):
        self.adjacentList = adjacentList
    def addAdjacent(self, adjacent):
        self.adjacentList.append(adjacent)
        
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setH(self,h):
        self.h = h
    def setF(self,f):
        self.f = f
    def setG(self,g):
        self.g = g
    def setParent(self, parent):
        self.parent = parent

# vim: ts=4 et tw=79 cc=+1
