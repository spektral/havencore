#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Class for handling sprite animation.

"""

import pygame
from pygame.locals import *
from math import floor
from animation import Animation

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

class RotSprite(Animation):
    def set_direction(self, angle):
        self.current_frame = self.angle_to_index(angle)

    def angle_to_index(self, angle):
        slice_size = (self.frame_count / 360.0)
        index = int(floor(slice_size * (angle + 22.5))) % self.frame_count
        return index



if __name__ == "__main__":
    # Unit test
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    # Create animation from the file with width and height 80
    anim = RotSprite("img/missile2.png", (32, 32))

    print("Frame count: %d" % anim.frame_count)
    print("Frame size: (%d, %d)" % (anim.w, anim.h))

    is_running = True
    direction = 0
    while is_running:
        # Rotate the animation 10 frames per second
        direction = (direction + 1)
        anim.set_direction(direction)

        screen.fill(pygame.Color(0, 0, 0))

        anim.draw(screen, 320, 240)

        pygame.time.delay(5)
        pygame.display.update()

        # Quit on any key
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                is_running = False
                break

# vim: set ts=4 sw=4 et
