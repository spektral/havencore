#!/usr/bin python
#coding=UTF-8
#========================================================================
# File: explode.py
#
# Author: Max Sidenstjärna
# Date: 2011-10-24
# Licens: GPL
#
# Comment:
#
#========================================================================

import pygame
import entity
import gameengine
import animation

class Explosion(entity.Entity):
    def __init__(self, x, y, filename, size, frame_delay):
        entity.Entity.__init__(self, x, y, size[0] / 2)
        self.animation = animation.Animation(filename, size, frame_delay)
        self.animation.loop = False
        self.is_collidable = False
    
    def handle_input(self, event):
        pass

    def update(self): 
        self.animation.update()
        if self.animation.finished == True:
            self.alive = False

    def draw(self, screen):
        self.animation.draw(screen, self.x, self.y)
