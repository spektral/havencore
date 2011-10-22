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

    def handle_input(self, event):
        pass

    def update(self):
        self.x_pos += self.vel * math.sin(self.rot)
        self.y_pos += self.vel * math.cos(self.rot)

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color(255,255,255), (int(self.x_pos),int(self.y_pos)), 2)

    def __repr__(self):
        return str(self.x_pos) 

# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    test.update()
    print test
