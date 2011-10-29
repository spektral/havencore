#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

from math import floor, radians, sin, cos
import pygame
from pygame.locals import *
from gameengine import gameengine

__author__    = "Gustav Fahlén, Max Sidenstjärna, Christofer Odén"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"


class Entity(object):

    """Abstract base class for data belonging to all kinds of of game
    objects."""

    ticker = 0

    def __init__(self, player, (x, y), r):
        self.serial = Entity.ticker
        Entity.ticker += 1
        self.age = 0
        self.player = player
        self.x = x
        self.y = y
        self.r = r
        self.collision_list = []
        self.is_collidable = True
        self.alive = True

    def update(self):
        self.age += 1

    def get_state(self):

        """Return a dictionary representation of the instance."""

        # Get the state of the object
        state = { 'type': 'entity',
                 'name': self.__class__.__name__,
                 'dict': dict(self.__dict__) }

        # Weed out unnecessary fields
        try:
            del state['dict']['children']
        except KeyError:
            pass

        try:
            del state['dict']['parent']
        except KeyError:
            pass

        try:
            del state['dict']['collision_list']
        except KeyError:
            pass

        return state

    def check_collisions(self, entities):
        for entity in entities:
            if entity is not self and entity.is_collidable:
                dx = entity.x - self.x
                dy = entity.y - self.y
                rr = (entity.r + self.r) / 2
                if dx * dx + dy * dy < rr * rr:
                    self.collision_list.append(entity)


class Vehicle(Entity):

    """Generic class for all types of vehicles in the game"""

    def __init__(self, player, (x, y), rot):
        Entity.__init__(self, player, (x, y), 40)
        self.rot = rot

        self.torque = 0
        self.vel = 0

        self.health = 100

        self.children = []

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.vel += 5.0

            if event.key == K_DOWN:
                self.vel -= 5.0

            if event.key == K_RIGHT:
                self.torque -= 5.0

            if event.key == K_LEFT:
                self.torque += 5.0

            if event.key == K_SPACE:
                self.fire()

        elif event.type == KEYUP:
            if event.key == K_UP:
                self.vel -= 5.0

            if event.key == K_DOWN:
                self.vel += 5.0

            if event.key == K_RIGHT:
                self.torque += 5.0

            if event.key == K_LEFT:
                self.torque -= 5.0

    def update(self):
        Entity.update(self)

        while self.collision_list:
            entity = self.collision_list.pop(0)
            if not entity in self.children \
                    and isinstance(entity, Missile):
                self.health -= 40

        self.children = [c for c in self.children if c.alive]


        if self.health <= 0:
            self.alive = False
        self.rot += self.torque

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.x += (self.vel * sin(radians(self.rot)))
        self.y += (self.vel * cos(radians(self.rot)))

    def fire(self):
        missile = Missile(self.player, (self.x, self.y), 12, self.rot,
                          (32, 32), self)
        gameengine.add_entity(missile) 
        self.children.append(missile)

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Missile(Entity):

    """Generic class for all projectiles in the game."""

    def __init__(self, player, (x, y), vel, rot, size, parent):
        """Initialize itself and it's base class."""
        Entity.__init__(self, player, (x, y), size[0] / 2)
        self.vel = vel
        self.rot = rot
        self.parent = parent

    def handle_input(self, event):
        """Handle external manipulation."""
        pass

    def update(self):

        """Do logic, react to collisions, move."""

        Entity.update(self)
        if self.age > 50:
            self.alive = False

        for entity in self.collision_list:
            if entity is not self.parent:
                self.alive = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def __repr__(self):
        """Return a string representation of the instance."""
        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


# vim: ts=4 et tw=79 cc=+1
