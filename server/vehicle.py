#!/usr/bin/python2 -tt
#coding=UTF-8
#--------------------------------------
#Name: vehicle.py
#Class for the vehicles, handles
#input, update, draw...
#
#Gustav Fahlén, 2011-10-22
#-------------------------------------

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import json
from math import floor, radians, sin, cos
import pygame
from pygame.locals import *
from gameengine import gameengine
from entity import Entity
from missile import Missile


class Vehicle(Entity):
    def __init__(self, player, (x, y), rot):
        Entity.__init__(self, player, (x, y), 40)
        self.rot = rot

        self.torque = 0
        self.vel = 0

        self.health = 100

        self.children = []

    def handle_input(self, event):
        #print("%s.handle_input(%s)" % (self.__class__.__name__,
        #                               event))
        #print("%s.player=%s" % (self.__class__.__name__, self.player))
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


#
#   Unit test procedure
#
if __name__ == "__main__":
    pass

# vim: ts=4 et tw=79 cc=+1
