#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

from math import floor, radians, sin, cos
import logging

from random import randint

import pygame
from pygame.locals import *

from gameengine import gameengine
import sqlite3

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
        blacklist = ['children', 'parent', 'collision_list', 'logger']

        for item in blacklist:
            try:
                del state['dict'][item]
            except KeyError:
                pass

        return state

    def get_colliders(self):
        return self.collision_list

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

    def __init__(self, player, (x, y), rot, modules):
        self.logger = logging.getLogger('server.entities.Vehicle')

        Entity.__init__(self, player, (x, y), 60)
        self.rot = rot
        self.maxvel = 0
        self.torque = 0
        self.vel = 0
        self.strafe_vel = 0

        # Fire control
        self.is_firing = False
        self.fire_delay = 25
        self.cooldown = 0
        
        #some standard values
        self.speed = 1

        self.health = 100
       
        self.active_modules = []
        #change standard values according to what modules vehicle is built of. 
        self.set_modules(modules)
        self.children = []
        self.logger.debug("HP: %s  Speed: %s" %
                          (self.health, self.speed))

    def set_modules(self, modules):
        conn = sqlite3.connect('server/havencore.db')
        c = conn.cursor()
        c.execute('select * from modules')
        for module in c:
            if module[0] in modules:
                if module[0] not in self.active_modules:
                    self.active_modules.append(module[0]) #Append the module
                
                if module[1] == 'speed': #this module changes speed
                    self.speed += module[2]
                elif module[1] == 'armor':
                    self.health += module[2]

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.vel += self.speed

            if event.key == K_s:
                self.vel -= self.speed

            if event.key == K_d:
                self.strafe_vel -= self.speed

            if event.key == K_a:
                self.strafe_vel += self.speed

            if event.key == K_LEFT:
                self.torque += self.speed

            if event.key == K_RIGHT:
                self.torque -= self.speed

            if event.key == K_SPACE:
                self.is_firing = True

        elif event.type == KEYUP:
            if event.key == K_w:
                self.vel -= self.speed

            if event.key == K_s:
                self.vel += self.speed

            if event.key == K_d:
                self.strafe_vel += self.speed

            if event.key == K_a:
                self.strafe_vel -= self.speed

            if event.key == K_LEFT:
                self.torque -= self.speed

            if event.key == K_RIGHT:
                self.torque += self.speed

            if event.key == K_SPACE:
                self.is_firing = False

    def update(self):
        Entity.update(self)

        while self.collision_list:
            entity = self.collision_list.pop(0)
            if not entity in self.children and isinstance(entity, Missile):
                self.health -= 5

        self.children = [c for c in self.children if c.alive]


        if self.health <= 0:
            self.alive = False
        self.rot += self.torque / 4.0

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.x += (self.vel * sin(radians(self.rot))) / 2.0
        self.y += (self.vel * cos(radians(self.rot))) / 2.0
        self.x += (self.strafe_vel * sin(radians(self.rot + 90.0))) / 2.0
        self.y += (self.strafe_vel * cos(radians(self.rot + 90.0))) / 2.0

        # Fire control
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0

        if self.is_firing and self.cooldown == 0:
            self.fire()
            self.cooldown = self.fire_delay

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
        self.rot = rot + randint(-10, 10)
        self.parent = parent
        self.max_age = randint(20, 50)

    def handle_input(self, event):
        """Handle external manipulation."""
        pass

    def update(self):

        """Do logic, react to collisions, move."""

        Entity.update(self)
        if self.age > self.max_age:
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
