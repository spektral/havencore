#!/usr/bin python
#coding=UTF-8
#========================================================================
# File: missile.py
#
# Author: Max Sidenstjärna
# Date: 2011-10-22
# Licens: GPL
#
# Comment:
#
#========================================================================

import gameengine
import pygame
import explosion
import entity
import rotsprite
import math
from math import floor, radians

class Missile(entity.Entity):
    
    def __init__(self, x, y, vel, rot):
        super(Missile, self).__init__(x, y, 16)
        self.vel = vel
        self.rot = rot
        
        self.unit = rotsprite.RotSprite("img/missile2.png", (32, 32))
        self.unit.set_direction(self.rot)

    def handle_input(self, event):
        pass

    def update(self):
        if not self.collision_list == []:
            GameEngine().entities.remove(self)
            GameEngine().entities.append(Explosion(self.x, self.y,
                "img/explosion2.png", (64, 64), 2))
            self.collision_list = []

        self.x_pos += self.vel * math.sin(radians(self.rot))
        self.y_pos += self.vel * math.cos(radians(self.rot))

    def draw(self, screen):
        self.unit.draw(screen, self.x_pos, self.y_pos)

    def __repr__(self):
        return str(self.x_pos)



# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    #test.update()
    print test
