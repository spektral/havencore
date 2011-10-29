#!/usr/bin python
#coding=UTF-8
#========================================================================
# File: missile.py
#
# Author: Max Sidenstjärna
# Date: 2011-10-22
# Licens: GPL
#
# Comment:
#
#========================================================================

from math import floor, radians, sin, cos
from gameengine import gameengine
from entity import Entity

__author__    = "Max Sidenstjärna"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

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
