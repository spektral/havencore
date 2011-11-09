#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Classes for game entities.

"""

from math import *
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


def look_at((eye_x, eye_y), (tgt_x, tgt_y)):

    """Calculate the angle of a vector"""

    nx = tgt_x - eye_x
    ny = tgt_y - eye_y

    cx, cy = (0, 1)

    norm = sqrt(nx * nx + ny * ny)
    (nx, ny) = (nx / norm, ny / norm)

    dot = nx * cx + ny * cy

    if nx < 0:
        return degrees(acos(-dot)) + 180
    else:
        return degrees(acos(dot))


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
        self.turret = Turret(parent=self, offset=0,
                sprite=spritemaps['turret'])

    def handle_input(self, event):
        self.turret.handle_input(event)

    def update(self):
        if not self.alive and self.alive_locally:
            jukebox.play_sound('vehicle_boom')
            self.logger.info("%s died!" % self.player)
            self.health = 0
            entity_container.append(LOCAL,
                    Explosion((self.x, self.y),
                              spritemaps['vehicle_explosion'], 10))
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

        self.turret.update()
        self.sprite.set_direction(self.rot)

    def draw(self, x, y):
        screen = display.get_surface()
        self.sprite.draw(screen, (x, y))
        self.turret.draw()

    def get_health(self):
        return self.health

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Turret:
    def __init__(self, parent, offset, sprite):
        self.logger = logging.getLogger('client.entities.Turret')
        self.parent = parent
        self.offset = offset
        self.rot = 0

        self.x = self.parent.x + self.offset * sin(radians(self.parent.rot))
        self.y = self.parent.y + self.offset * cos(radians(self.parent.rot))

        self.sprite = RotSprite(sprite)
        self.alive_locally = True

    def handle_input(self, event):
        if event.type == MOUSEMOTION:
            self.rot = look_at((self.x, self.y), event.pos)

    def update(self):
        if not self.parent.alive_locally:
            self.alive_locally = False

        self.x = self.parent.x + self.offset * sin(radians(self.parent.rot))
        self.y = self.parent.y + self.offset * cos(radians(self.parent.rot))

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.sprite.set_direction(self.rot)

    def draw(self, x, y)
        screen = display.get_surface()
        self.sprite.draw(screen, x, y)


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
                        spritemaps['missile_explosion'], 4))
            self.alive_locally = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))
        self.sprite.set_direction(self.rot)

    def draw(self, x, y):
        screen = display.get_surface()
        self.sprite.draw(screen, x, y)

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

    def handle_input(self, event):
        pass

    def update(self):
        if not self.alive and self.alive_locally:
            self.alive_locally = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def draw(self, x, y):
        screen = display.get_surface()
        pygame.draw.circle(screen, (0,0,0), (int(x + 0.5),int(y + 0.5)), 2)

    def __repr__(self):
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))

class LandMine:

    """Generic class for all LandMines in the game."""

    def __init__(self, dict):
        self.__dict__ = dict
        self.alive_locally = True

    def handle_input(self, event):
        pass

    def update(self):
        if not self.alive and self.alive_locally:
            jukebox.play_sound('missile_boom')
            entity_container.append(
                    LOCAL,
                    Explosion((self.x, self.y),
                        spritemaps['missile_explosion'], 4))
            self.alive_locally = False

    def draw(self, x, y):
        screen = display.get_surface()
        pygame.draw.circle(screen, (0,142,250), (int(x),int(y)), 10)

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
        if self.animation.visible == False:
            self.alive = False

    def draw(self, x, y):
        screen = display.get_surface()
        self.animation.draw(screen, x, y)

# vim: ts=4 et tw=79 cc=+1
