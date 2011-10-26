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
        super(Explosion, self).__init__(x, y, 32)
        self.animation = animation.Animation(filename, size, frame_delay)
        self.animation.loop = False
        self.is_collidable = False
    
    def handle_input(self, event):
        pass

    def update(self): 
        self.animation.update()
        if self.animation.finished == True:
            GameEngine().entities.remove(self)

    def draw(self, screen):
        self.animation.draw(screen, self.x_pos, self.y_pos)
