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
import entity
import math
from math import floor, radians

class Missile(entity.Entity):
    
    def __init__(self, x_pos, y_pos, vel, rot):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = vel
        self.rot = rot
        self.img_rec_num = 40
        
        self.unit = self.load_sliced_sprites(32,32, 'img/missile2.png')
        self.unitIndex = self.spriteIndex(self.rot)
        
<<<<<<< HEAD
# !! Doesent need anymore pg. inherens from entity.py
# def load_sliced_sprites(self, w, h, filename):
# images = []
=======
# !! Doesent need anymore. inherates from entity.py
#    def load_sliced_sprites(self, w, h, filename):
#	images = []
>>>>>>> c7dbc1bfe4cd47485d184b9cc355176b183928f6
#
# master_image = pygame.image.load(filename).convert()
# #colorkey = (1,255,243)
# colorkey = master_image.get_at((0,0))
# master_image.set_colorkey(colorkey, pygame.RLEACCEL)
#
<<<<<<< HEAD
# master_width, master_height = master_image.get_size()
#
# for i in xrange(int(master_width/w)):
# images.append(master_image.subsurface((i*w,0,w,h)))
# return images
#------------------------------------------------------

    def spriteIndex(self,v):
	C = (40.0/360.0) #C=(8.0/360.0) för 8 bilder
	index = int(floor((C*(v+22.5)))) % 40
	return index

=======
#	master_width, master_height = master_image.get_size()
#        
#        for i in xrange(int(master_width/w)):
#		images.append(master_image.subsurface((i*w,0,w,h)))
#	return images
#
#------------------------------------------------------
#
#    def spriteIndex(self,v):
#	C = (40.0/360.0) #C=(8.0/360.0) för 8 bilder 
#	index = int(floor((C*(v+22.5)))) % 40 
#	return index
#======================================================
>>>>>>> c7dbc1bfe4cd47485d184b9cc355176b183928f6

    def handle_input(self, event):
        pass


    def update(self):
        self.x_pos += self.vel * math.sin(radians(self.rot))
        self.y_pos += self.vel * math.cos(radians(self.rot))
        
        
    def collide_detect(self, lst_ent):
        for ent in lst_ent:
            if self is not ent:
                x_sum = self.x_pos-ent.x_pos
                x_sum = x_sum * x_sum
                y_sum = self.y_pos-ent.y_pos
                y_sum = y_sum * y_sum

                if math.sqrt(x_sum+y_sum) < 56:
                    return 1
                else:
                    return 0

    def draw(self, screen):
        #pygame.draw.circle(screen, pygame.Color(255,255,255), (int(self.x_pos),int(self.y_pos)), 2)
        screen.blit(self.unit[self.unitIndex], (self.x_pos-16,self.y_pos-16) )

    def __repr__(self):
        return str(self.x_pos)

# Debug main
if __name__=="__main__":
    test = Missile(2,3,4,1)
    print test
    #test.update()
    print test
