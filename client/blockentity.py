# -*- coding: utf-8 -*-
import pygame 
from defines import *
from entities import Entity

"""
Generic class for all projectiles in the game.

"""
class BlockEntity(Entity):
    #def __init__(self, (x,y), vel, rot, filename, size, parent):
    def __init__(self, (x,y), vel, rot, (r,g,b), size, parent):
        Entity.__init__(self, (x, y), size*2)
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
    def is_walkable(self):
        if self.color == black:
            return 0
        return 1
    def toString(self):
        return str(self.x) + " " + str(self.y)+ " " + str(self.color) + " " + str(self.size) + "\n"
    def set_color(self,color):
        self.color = color
        
           
               
    def draw(self,screen, x_offset = 0, y_offset = 0):
        pygame.draw.rect(screen,self.color,(( self.x+x_offset, self.y+y_offset), (self.size-2,self.size-2)))
        
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
    
    def get_adjacent_list(self):
        return self.adjacentList
    
    def set_adjacent_list(self, adjacent_list):
        self.adjacentList = adjacent_list
    def addAdjacent(self, adjacent):
        self.adjacentList.append(adjacent)
        
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def set_h(self,h):
        self.h = h
    def setF(self,f):
        self.f = f
    def setG(self,g):
        self.g = g
    def setParent(self, parent):
        self.parent = parent

# vim: ts=4 et tw=79 cc=+1
