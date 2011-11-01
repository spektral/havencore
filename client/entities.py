#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Classes for game entities.

"""

from math import floor, radians, sin, cos
from os import path

import logging

import pygame
from pygame.locals import *

from jukebox import jukebox
from graphics import *

__author__   = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"


class Entity:
    def __init__(self, (x, y), r):
        self.x = x
        self.y = y
        self.r = r


class Vehicle:
    def __init__(self, dict, filename, size):
        self.__dict__ = dict
        self.sprite = RotSprite(filename, (128,128))
        self.logger = logging.getLogger('client.entities.Vehicle')

    def update(self):
        if self.health <= 0:
            jukebox.play_sound('vehicle_boom')
            self.logger.info("%s died!" % self.player)
            self.health = 0
            #filename = path.join(path.dirname(__file__), "/img/explosion2.png")
            #gameengine.add_local(Explosion((self.x, self.y), filename
                                           #(64, 64), 2))
            self.alive = False

        self.rot += self.torque

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.x += (self.vel * sin(radians(self.rot)))
        self.y += (self.vel * cos(radians(self.rot)))
        self.sprite.set_direction(self.rot)

    def draw(self, screen):
        self.sprite.draw(screen, self.x, self.y)

    def fire(self):
        pass

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Missile:

    """
    Generic class for all projectiles in the game.

    """

    def __init__(self, dict, filename, size):
        self.__dict__ = dict
        self.sprite = RotSprite(filename, size)
        self.sprite.set_direction(self.rot)

    def handle_input(self, event):
        pass

    def update(self):
        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def draw(self, screen):
        self.sprite.draw(screen, self.x, self.y)

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Explosion(Entity):
    def __init__(self, (x, y), filename, size, frame_delay):
        Entity.__init__(self, (x, y), size[0] / 2) 
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


# vim: ts=4 et tw=79 cc=+1
