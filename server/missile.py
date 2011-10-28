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

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import entity
from gameengine import gameengine
from math import floor, radians, sin, cos

class Missile(entity.Entity):

    """Generic class for all projectiles in the game."""

    def __init__(self, (x, y), vel, rot, size, parent):
        """Initialize itself and it's base class."""
        entity.Entity.__init__(self, (x, y), size[0] / 2)
        self.vel = vel
        self.rot = rot
        self.parent = parent

    def handle_input(self, event):
        """Handle external manipulation."""
        pass

    def update(self):
        """Do logic, react to collisions, move."""
        for entity in self.collision_list:
            if entity is not self.parent:
                self.alive = False

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def get_state(self):
        """Return where the object is, what way it's facing etc."""
        return (self.x, self.y, self.vel, self.rot)

    def __repr__(self):
        return ("(Missile, rot: %.2f, vel: %.2f, (x%.2f, y%.2f))" %
            (self.rot, self.vel, self.x, self.y))
