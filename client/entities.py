#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Classes for game entities.

"""

from math import floor, radians, sin, cos
from os import path

import logging

import pygame
from pygame import display
from pygame.locals import *

from jukebox import jukebox
from graphics import *

from entitylist import entity_container
from entitylist import *

__author__   = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"


class Entity:
    def __init__(self, (x, y), r):
        self.x = x
        self.y = y
        self.r = r
        self.alive = True


class Vehicle:
    def __init__(self, dict, sprite):
        self.__dict__ = dict
        self.logger = logging.getLogger('client.entities.Vehicle')
        self.sprite = RotSprite(sprite)
        self.alive_locally = True

    def update(self):
        if not self.alive and self.alive_locally:
            jukebox.play_sound('vehicle_boom')
            self.logger.info("%s died!" % self.player)
            self.health = 0
            entity_container.append(LOCAL,
                    Explosion((self.x, self.y),
                              sprites['vehicle_explosion'], 10))
            self.alive_locally = False

        #self.rot += self.torque / 4.0

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

#        self.x += (self.vel * sin(radians(self.rot))) / 2.0
#        self.y += (self.vel * cos(radians(self.rot))) / 2.0
#        self.x += (self.strafe_vel * sin(radians(self.rot + 90.0))) / 2.0
#        self.y += (self.strafe_vel * cos(radians(self.rot + 90.0))) / 2.0
        self.sprite.set_direction(self.rot)

    def draw(self):
        screen = display.get_surface()
        self.sprite.draw(screen, self.x, self.y)

    def get_health(self):
        return self.health

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Missile:

    """Generic class for all projectiles in the game."""

    def __init__(self, dict, sprite):
        self.__dict__ = dict
        self.sprite = RotSprite(sprite)
        self.sprite.set_direction(self.rot)
        self.alive_locally = True

    def handle_input(self, event):
        pass

    def update(self):
        if not self.alive and self.alive_locally:
            jukebox.play_sound('missile_boom')
            entity_container.append(
                    LOCAL,
                    Explosion((self.x, self.y),
                        sprites['missile_explosion'], 4))
            self.alive_locally = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))
        self.sprite.set_direction(self.rot)

    def draw(self):
        screen = display.get_surface()
        self.sprite.draw(screen, self.x, self.y)

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Machinegun:

    """Generic class for Machingun bullets in the game."""

    def __init__(self, dict):
        self.__dict__ = dict
        self.alive_locally = True

    def handle_input(self):
        pass

    def update(self):
        if not self.alive and self.alive_locally:
            self.alive_locally = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def draw(self):
        screen = display.get_surface()
        pygame.draw.circle(screen, (0,0,0), (int(self.x + 0.5),int(self.y + 0.5)), 2)

    def __repr__(self):
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))

class LandMine:

    """Generic class for all LandMines in the game."""

    def __init__(self, dict):
        self.__dict__ = dict
        self.alive_locally = True

    def handle_input(self):
        pass

    def update(self):
        if not self.alive and self.alive_locally:
            jukebox.play_sound('missile_boom')
            entity_container.append(
                    LOCAL,
                    Explosion((self.x, self.y),
                        sprites['missile_explosion'], 4))
            self.alive_locally = False

    def draw(self):
        screen = display.get_surface()
        pygame.draw.circle(screen, (0,142,250), (int(self.x),int(self.y)), 10)

    def __repr__(self):
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))

class Explosion(Entity):

    """Display an explosion, die when animation is finished"""

    def __init__(self, (x, y), sprite, frame_delay):
        Entity.__init__(self, (x, y), sprite['size'][0] / 2) 
        self.animation = Animation(sprite, frame_delay)
        self.animation.loop = False
        self.is_collidable = False
    
    def handle_input(self, event):
        pass

    def update(self): 
        self.animation.update()
        if self.animation.finished == True:
            self.alive = False

    def draw(self):
        screen = display.get_surface()
        self.animation.draw(screen, self.x, self.y)

# vim: ts=4 et tw=79 cc=+1
