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

import pygame
import explosion
import entity
import rotsprite
import math
import gameengine
from math import floor, radians

class Missile(entity.Entity):
    
    def __init__(self, x, y, vel, rot):
        entity.Entity.__init__(self, x, y, 16)
        self.vel = vel
        self.rot = rot
        
        self.unit = rotsprite.RotSprite("img/missile2.png", (32, 32))
        self.unit.set_direction(self.rot)

    def handle_input(self, event):
        pass

    def update(self):
        ge = gameengine.GameEngine()

        if not self.collision_list == []:
            print("Missile entities: %s" % ge.entities)
            ge.entities.append(explosion.Explosion(self.x, self.y,
                "img/explosion2.png", (64, 64), 2))
            print("Missile entities 2: %s" % ge.entities)

            self.alive = False

        self.x += self.vel * math.sin(radians(self.rot))
        self.y += self.vel * math.cos(radians(self.rot))

    def draw(self, screen):
        self.unit.draw(screen, self.x, self.y)

    def __repr__(self):
        return ("(Missile, rot: %.2f, vel: %.2f, (x%.2f, y%.2f))" %
            (self.rot, self.vel, self.x, self.y))



# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    #test.update()
    print test
