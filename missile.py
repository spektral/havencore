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

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import pygame
import explosion
import entity
import rotsprite
from gameengine import gameengine
from math import floor, radians, sin, cos

class Missile(entity.Entity):
    """
    Generic class for all projectiles in the game.

    """
    def __init__(self, x, y, vel, rot, filename, size, parent):
        entity.Entity.__init__(self, x, y, size[0] / 2)
        self.vel = vel
        self.rot = rot
        self.parent = parent
        
        self.unit = rotsprite.RotSprite(filename, size)
        self.unit.set_direction(self.rot)

    def handle_input(self, event):
        pass

    def update(self):
        for entity in self.collision_list:
            if entity is not self.parent:
                gameengine.add_entity(explosion.Explosion(self.x, self.y,
                    "img/explosion2.png", (64, 64), 2))
                self.alive = False
                gameengine.JukeBox.playSound('rocket')
			
        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def draw(self, screen):
        self.unit.draw(screen, self.x, self.y)

    def __repr__(self):
        return ("(Missile, rot: %.2f, vel: %.2f, (x%.2f, y%.2f))" %
            (self.rot, self.vel, self.x, self.y))
