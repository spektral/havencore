#!/usr/bin python
#coding=UTF-8
#==============================================================================
# File: missile.py
#
# Author: Max Sidenstjärna
# Date: 2011-10-22
# Licens: GPL
#
# Comment: 
#
#==============================================================================

import pygame
import entity
import math

class Missile(entity.Entity):
    
    def __init__(self, x_pos, y_pos, vel, rot):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = vel
        self.rot = rot
        
        self.image = pygame.image.load("img/missil_2.png")
        
        #self.image = self.image.convert()
        #self.image.set_colorkey((1,255,234), RLEACCEL)
        #self.rect = self.image.get_rect()

    def handle_input(self, event):
        pass

    def update(self):
        self.x_pos += self.vel * math.sin(self.rot)
        self.y_pos += self.vel * math.cos(self.rot)
        
        
    def collide_detect(self, lst_ent):
        for ent in lst_ent:
            if self is not ent:
                x_sum = self.x_pos-ent.x_pos
                x_sum = x_sum * x_sum
                y_sum = self.y_pos-ent.y_pos
                y_sum = y_sum * y_sum

                if math.sqrt(x_sum+y_sum) < 22:
                    return 1
                else:
                    return 0

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(255,255,255), (int(self.x_pos),int(self.y_pos)), 2)
        screen.blit(self.image, (self.x_pos-2,self.y_pos-2) )

    def __repr__(self):
        return str(self.x_pos) 

# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    #test.update()
    print test
