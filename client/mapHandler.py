# -*- coding: utf-8 -*-
import pygame
import random
import math
import time
#
from defines import *
from blockentity import BlockEntity
#from filehandler import *



class MapHandler:
    def __init__(self,width, height, blockSize):
        self.screen = 0
        self.width = width
        self.height = height
        self.blockSize = blockSize
        self.blockList = []
        self.init_blockList()
        self.init_adjacent()
        
        # for painting and illustrating of algorithms:
        self.illustrate = True
        self.delay = DELAY
        self.changed = self.blockList 

    def set_screen(self, screen):
        self.screen = screen
    def init_blockList(self):
        for j in range(self.height/self.blockSize):
            for i in range(self.width/self.blockSize):
                self.blockList.append(BlockEntity((i*self.blockSize, j*self.blockSize), 0, 0, white, self.blockSize, None))
           # to be used.
           #    self.blockList.append(BlockEntity((i*self.blockSize, j*self.blockSize), 0, 0, "", self.blockSize, None):
    def handle_input(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #self.start = self.get_block_at(self.get_block_index(pygame.mouse.get_pos()))
            
            self.get_block_at(pygame.mouse.get_pos()).set_color(black)
            #paint all colliding.
            #collider =self.get_block_at(self.get_block_index(pygame.mouse.get_pos()))
            #collider.check_collisions(self.blockList)
            #for colliding in collider.collision_list:
            #    colliding.set_color(red)

       
        #if event.type == pygame.MOUSEBUTTONUP:
            #self.end = self.get_block_at(self.get_block_index(pygame.mouse.get_pos()))
            #self.calc_path(self.start, self.end)

    def clear(self):
        self.blockList = []
        self.init_blockList()
        self.init_adjacent()
        self.changed = self.blockList
    def init_adjacent(self):
      #  for block in self.blockList:
            #block.check_collisions(self.blockList)
           # block.set_adjacent_list(block.get_colliders())
        print "wtf.."
    def get_block_at(self,i):
            return self.blockList[i]
    def get_block_at(self, (x,y)):
            return self.blockList[self.get_block_index((x,y))]
    def get_block_index(self, (x,y)): 
        return ((y/self.blockSize)*(self.width/self.blockSize)) + (x/self.blockSize)# +( y/self.blockSize)
       
    def right_pos(self,(x,y)):
        return ((x/self.blockSize)*self.blockSize,(y/self.blockSize)*self.blockSize)
        
   
   # Refactaway?
    def fill_correct(self): 
        self.blockList[self.get_block_index(pygame.mouse.get_pos())].setColor(colorList[0])
    def random_fill(self):
        #self.blockList[0].setColor(red)
        self.changed.append(random.choice(self.blockList))
        self.changed[len(self.changed)-1].setColor(random.choice(colorList))
        #random.choice(self.blockList).setColor(random.choice(colorList))
        
    def draw(self, screen):
        # HACK
        self.screen = screen
        #self.random_fill()
     
        self.draw_board(screen)
        # this will n
        for c in self.blockList: 
            c.draw(screen)
        self.changed = []
    def update_all(self):
        self.changed = self.blockList
    def draw_board(self,screen):    
        p = 0
        for i in range(0, self.width/self.blockSize):
            pygame.draw.line(screen, red, (p, 0), (p,self.height), 1)
            p = p+self.blockSize
        p = 0
        for i in range(0,self.height/self.blockSize):
            pygame.draw.line(screen, red, (0,p), (self.width,p), 1)
            p = p+self.blockSize
               
    def remove_colliding(self, block):
            for t in self.blockList:
                if block.x == t.x and block.y == t.y:
                    self.blockList.remove(t)
                    
    def change_color_at(self, i, color):
        self.changed.append(self.blockList[i])
        self.blockList[i].setColor(color)
    
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_block_size(self):
        return self.blockSize
    def get_block_list(self):    
        return self.blockList
    def is_walkable(self, (x,y)):
        return self.get_block_at(self.get_block_index(x,y)).is_walkable()
    #def saveMap(self, filename):
    #    f = FileHandler()
    #    f.writeList(filename, self.blockList)
   # def loadMap(self, filename):
  #      f = FileHandler()
   #     self.blockList = f.readFile("out.txt")
        
    #    selfinit_adjacent()
    #    self.changed = self.blockList
    def testCalc(self):
        self.calc_path(self.blockList[0],self.blockList[1])
    # THIS RETURNS THE BEST PATH
    # AS A LIST OF BLOCKS!
    # (ATM WE CANT GO DIAGONAL)
    def calc_path(self, startBlock, endBlock):
        if endBlock.is_walkable() == 0:
            return None
        self.closedList = []
        self.openList = []
        self.beforeList = list(self.blockList) #save the old list...
        endBlock.set_color(pink)
        s = startBlock
        #self.openList.append(startBlock) 
        tid = time.clock()
        t = self.a_star(startBlock,endBlock)

        #t = self.dijkstra(startBlock, endBlock)
        tid =  time.clock() - tid
       # print tid
        i = t
        
        illuList = []
        while t != s:
            if t == None:
                return t
            t.set_color(pink)
            illuList.append(t)
            t = t.getParent()
            
        s.set_color(pink)
        illuList.append(s)
        illuList.reverse()
        for block in illuList:
             block.draw(self.screen)
             pygame.display.flip()
             #time.sleep(self.delay)
             
        return i
    
    
 
    def a_star(self, startBlock, endBlock):
        closedList = []
        openList = []
        came_from = "the empty map?" # :D
        openList.append(startBlock)
        
        #startBlock.setH(self.calc_manhattan(startBlock, endBlock))
        #startBlock.setF(startBlock.getG()+startBlock.getH())
        startBlock.setG(0)
        while len(openList) != 0:
            
            self.calc_heuristic(openList, endBlock)
            
            x = openList[0] # BEST BLOCK, HACK
            for block in openList:
                block.setG(startBlock.getG()+10)
                block.setF(block.getG()+block.getH())
                if x.getF() > block.getF():
                    x = block
            if x == endBlock:
                return x
            
            closedList.append(x)
            openList.remove(x)
            self.calc_heuristic(x.get_adjacent_list(),endBlock)
            for block in x.get_adjacent_list():
                
                if block in closedList or block.is_walkable() == 0:
                    continue
                tentativeG = block.getG()+x.getG() # 10pts for the move
                better = False
                if block not in openList:
                    openList.append(block)
                    better = True
                elif tentativeG < block.getG() or block.getG() == 0:
                    better = True
                if better == True:
                    block.setParent(x)
                    block.setG(tentativeG)
                    block.set_h(self.calc_manhattan(block,endBlock))
                    block.setF(block.getG()+block.getH())
      
        
           
       #return self.recSearch(
        
    
    def calc_heuristic(self, blockSet, endBlock):
        for block in blockSet:
            block.set_h(self.calc_manhattan(block, endBlock))
            
    # CALC H THE MANHATTAN WAY
    def calc_manhattan(self, startBlock, endBlock):
       #FIXED ALOT BY DIVIDE
        return 10*(abs(startBlock.getX()/self.width-endBlock.getX()/self.width) + abs(startBlock.getY()/self.height-endBlock.getY()/self.height))
       
          
    #NOT WORKING YET
    def dijkstra(self,startBlock, endBlock):
        graph = self.blockList
        inf = 99999
        for vertex in graph:
            vertex.setF(inf)
            vertex.setParent(0)
        startBlock.setF(0)
        
        Q = graph
        while len(Q) != 0:
            
            u = Q[0]
            for vertex in Q:
                if vertex.getF() < u.getF():
                    u = vertex
                if vertex.getF() == inf:
                    break
                u.setColor(red)
                u.draw(self.screen)
                pygame.display.flip()
                Q.remove(u)
                for v in u.getAdjacentList():
                    alt = u.getF() + self.calc_manhattan(u, v)
                    if alt < u.getF():
                        v.setF(alt)
                        v.setParent(u)
                        Q.remove(v)
                    if v == endBlock:
                        return v
        
        

# vim: ts=4 et tw=79 cc=79 
