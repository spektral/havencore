#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Module for purely visual stuff.

"""

from math import floor

import pygame
from pygame.locals import *

__credits__   = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"


class Animation:

    """Class for handling sprite animation"""

    def __init__(self, filename, frame_size, delay=0):
        self.current_frame = 0
        self.ticker = 0
        self.delay = delay
        self.running = True
        self.loop = True
        self.finished = False

        self.load_image(filename, frame_size)

    def play(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.current_frame = 0

    def set_current_frame(self, index):
        assert(index < self.frame_count)
        self.current_frame = index

    def load_image(self, filename, frame_size):
        assert(isinstance(frame_size, tuple))

        image = pygame.image.load(filename).convert()

        # Set color key
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

        # Get animation frames
        self.frames = []
        img_width, img_height = image.get_size()
        self.w, self.h = frame_size
        self.frame_count = img_width / self.w;
        for i in range(self.frame_count):
            self.frames.append(image.subsurface((i * self.w, 0,
                                                 self.w, self.h)))

    def update(self):
        if self.running:
            self.ticker += 1
            if (self.ticker > self.delay):
                self.current_frame += 1
                if self.current_frame >= self.frame_count:
                    if self.loop == False:
                        self.finished = True
                    else:
                        self.current_frame = 0
                self.ticker = 0

    def draw(self, screen, x, y):
        if not self.finished:
            screen.blit(self.frames[self.current_frame],
                        (x - self.w / 2, y - self.h / 2))


class RotSprite(Animation):

    """Class for handling indexes of rotating sprites"""

    def set_direction(self, angle):
        self.current_frame = self.angle_to_index(angle)

    def angle_to_index(self, angle):
        slice_size = (self.frame_count / 360.0)
        index = int(floor(slice_size * (angle))) % self.frame_count
        return index


#class Explosion(Entity):
#    def __init__(self, (x, y), filename, size, frame_delay):
#        entity.Entity.__init__(self, (x, y), size[0] / 2)
#        self.animation = animation.Animation(filename, size, frame_delay)
#        self.animation.loop = False
#        self.is_collidable = False
#    
#    def handle_input(self, event):
#        pass
#
#    def update(self): 
#        self.animation.update()
#        if self.animation.finished == True:
#            self.alive = False
#
#    def draw(self, screen):
#        self.animation.draw(screen, self.x, self.y)


# vim: ts=4 et tw=79 cc=+1
