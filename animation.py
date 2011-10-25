#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Class for handling sprite animation.

"""

import pygame
from pygame.locals import *

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

class Animation:
    def __init__(self, filename, frame_size, delay=0):
        self.current_frame = 0
        self.ticker = 0
        self.delay = delay
        self.running = False

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
        self.ticker += 1
        if (self.ticker >= self.delay):
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                self.current_frame = 0
            self.ticker = 0

    def draw(self, screen, x, y):
        screen.blit(self.frames[self.current_frame],
                    (x - self.w / 2, y - self.h / 2))



if __name__ == "__main__":
    # Unit test
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    # Create animation from the file with width and height 80
    anim = Animation("img/explosion2.png", (64, 64), 2)

    print("Frame count: %d" % anim.frame_count)
    print("Frame size: (%d, %d)" % (anim.w, anim.h))

    is_running = True
    direction = 0
    while is_running:
        # Rotate the animation 10 frames per second
        anim.play()

        screen.fill(pygame.Color(0, 0, 0))

        anim.update()
        anim.draw(screen, 320, 240)

        pygame.time.delay(20)
        pygame.display.update()

        # Quit on any key
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                is_running = False
                break

# vim: set ts=4 sw=4 et
