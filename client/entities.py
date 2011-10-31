#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Classes for game entities.

"""

from math import floor, radians, sin, cos

import pygame
from pygame.locals import *

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
        self.collision_list = []
        self.is_collidable = True
        self.alive = True

    def handle_input(self, event):
        raise NotImplementedError("Not implemented")

    def update(self):
        raise NotImplementedError("Not implemented")

    def draw(self, screen):
        raise NotImplementedError("Not implemented")

    def check_collisions(self, entities):
        for entity in entities:
            if entity is not self and entity.is_collidable:
                dx = entity.x - self.x
                dy = entity.y - self.y
                rr = (entity.r + self.r) / 2
                if dx * dx + dy * dy < rr * rr:
                    self.collision_list.append(entity)


class Vehicle(Entity):
    def __init__(self, dict, filename, size):
        self.__dict__ = dict
        self.sprite = RotSprite(filename, (128,128))

#    def __init__(self, (x, y), rot):
#        Entity.__init__(self, (x, y), 40)
#        self.rot = rot
#        self.torque = 0
#        self.vel = 0
#        self.health = 100
#        self.children = []
#        gameengine.jukebox.load_sound('rocket.ogg','rocket')

#    def handle_input(self, event):
#        if event.type == KEYDOWN:
#            if event.key == K_UP:
#                self.vel += 2.0
#
#            if event.key == K_DOWN:
#                self.vel -= 2.0
#
#            if event.key == K_RIGHT:
#                self.torque -= 2.0
#
#            if event.key == K_LEFT:
#                self.torque += 2.0
#
            #if event.key == K_SPACE:
                #self.fire()
                #gameengine.jukebox.play_sound('rocket')
#
#        elif event.type == KEYUP:
#            if event.key == K_UP:
#                self.vel -= 2.0
#
#            if event.key == K_DOWN:
#                self.vel += 2.0
#
#            if event.key == K_RIGHT:
#                self.torque += 2.0
#
#            if event.key == K_LEFT:
#                self.torque -= 2.0

    def update(self):
#        while self.collision_list:
#            entity = self.collision_list.pop(0)
#            if not entity in self.children \
#                    and isinstance(entity, Missile):
#                self.health -= 40

#        self.children = [c for c in self.children if c.alive]

        if self.health <= 0:
            self.health = 0
            #gameengine.add_entity(Explosion((self.x, self.y),
                #"client/img/explosion2.png", (64, 64), 2))
            self.alive = False
            #gameengine.jukebox.play_sound('rocket')
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
        missile = Missile((self.x, self.y), 12, self.rot,
                "client/img/missile2.png", (32, 32), self)
        #gameengine.add_entity(missile) 
        self.children.append(missile)

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Missile(Entity):

    """
    Generic class for all projectiles in the game.

    """

    def __init__(self, dict, filename, size):
        self.__dict__ = dict
        self.sprite = RotSprite(filename, size)
        self.sprite.set_direction(self.rot)

#    def __init__(self, (x, y), vel, rot, filename, size, parent):
#        entity.Entity.__init__(self, (x, y), size[0] / 2)
#        self.vel = vel
#        self.rot = rot
#        self.parent = parent
#        
#        self.sprite = rotsprite.RotSprite(filename, size)
#        self.sprite.set_direction(self.rot)

    def handle_input(self, event):
        pass

    def update(self):
#        for entity in self.collision_list:
#            if entity is not self.parent:
#                gameengine.add_entity(explosion.Explosion((self.x, self.y),
#                    "client/img/explosion2.png", (64, 64), 2))
#                self.alive = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def draw(self, screen):
        self.sprite.draw(screen, self.x, self.y)

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


# vim: ts=4 et tw=79 cc=+1
