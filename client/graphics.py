#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Module for purely visual stuff.

"""

from os import path
from math import floor

import pygame
from pygame.locals import *

__credits__   = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"


class SpriteArray:

    """An integer indexable array of sprites based on an image file"""

    def __init__(self, spritemap, colorkeyed=True):
        self.sprites = []
        self.load_image(spritemap, colorkeyed)
        self.current_frame = 0
        self.visible = True
        self.sprite_w, self.sprite_h = spritemap['size']

    def load_image(self, spritemap, colorkeyed):

        """Load a sprite map image from file
        
        Add the sprites to the local sprite list.  Index the sprites
        based on their position in the image."""
        
        filename = spritemap['filename']
        sprite_size = spritemap['size']
        image = pygame.image.load(filename).convert()

        if colorkeyed:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        self.sprites = []
        img_w, img_h = image.get_size()
        sprite_w, sprite_h = sprite_size

        # Step through the image and add each consecutive sprite to
        # the sprite list
        for row in range(img_h / sprite_h):
            for col in range(img_w / sprite_w):
                img_x = col * sprite_w
                img_y = row * sprite_h
                self.sprites.append(image.subsurface(img_x, img_y,
                                                     sprite_w, sprite_h))

    def draw(self, screen, x, y):

        """Draw the current frame to screen"""

        if self.visible:
            screen.blit(self.sprites[self.current_frame],
                        (x - self.sprite_w / 2, y - self.sprite_h / 2))


class Animation(SpriteArray):

    """Class for handling sprite animation"""

    def __init__(self, spritemap, delay=0, loop=True):
        SpriteArray.__init__(self, spritemap)

        self.ticker = 0
        self.delay = delay
        self.running = True
        self.loop = loop

    def play(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.current_frame = 0

    def set_current_frame(self, index):
        self.current_frame = index

    def update(self):
        if self.running:
            self.ticker += 1
            if (self.ticker > self.delay):
                self.current_frame += 1
                if self.current_frame >= len(self.sprites):
                    if self.loop == False:
                        self.visible = False
                    else:
                        self.current_frame = 0
                self.ticker = 0


class RotSprite(SpriteArray):

    """Class for handling indexes of rotating sprites"""

    def set_direction(self, angle):
        self.current_frame = self.angle_to_index(angle)

    def angle_to_index(self, angle):
        slice_size = (len(self.sprites) / 360.0)
        index = int(floor(slice_size * (angle))) % len(self.sprites)
        return index


def add_spritemap(name, filename, size):

    """Add a sprite to the sprite container"""

    basedir = path.join(path.dirname(__file__), 'img')
    spritemaps[name] = {
            'filename': path.join(basedir, filename),
            'size': size
            }


def load_sprites():
    add_spritemap('vehicle',           'roller.png',          (128, 128))
    add_spritemap('turret',            'turret.png',          (128, 128))
    add_spritemap('missile',           'missile2.png',        (32, 32))
    add_spritemap('vehicle_explosion', 'blast.png',           (96, 96))
    add_spritemap('missile_explosion', 'explosion2.png',      (64, 64))
    add_spritemap('terrain',           'terrain.png',         (128, 128))


spritemaps = {}


# vim: ts=4 et tw=79 cc=+1
