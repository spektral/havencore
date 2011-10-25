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

class Explode(entity.Entity):

    def __init__(self, x_pos, y_pos, filename, num_rec, size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.index = 0
        self.unitIndex = 0
        self.size = size
        self.num_rec = num_rec
        self.unit = self.load_sliced_sprites(size,size, filename)

    def handle_input(self, event):
        pass

    def update(self): 
        self.index += 1
        
        # Here you can set the speed of the animation.
        # I think it looks best in full speed //eCo
        if self.index >= 1:
            self.unitIndex += 1
            self.index = 0

    def collide_detect(self, lst_ent):
        pass

    def draw(self, screen):
        screen.blit(self.unit[self.unitIndex], (self.x_pos-(self.size/2), self.y_pos-(self.size/2) ) )
