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

class Missile(entity.Entity):
    
    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.x_vel=x_vel
        self.y_vel=y_vel

    def handle_input(self, event):
        pass

    def update(self):
        self.x_pos+=self.x_vel
        self.y_pos+=self.y_vel

    def draw(self, screen):
        pygame.draw.circle(screen, white, (self.x_pos,self.y_pos), 2)
    
    def __repr__(self):
        return str(self.x_pos) 

# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    test.update()
    print test
