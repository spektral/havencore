#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Abstract base class for a common interface to all game objects.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import pygame
import math

class Entity:
    def __init__(self, x, y, r):
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



#
#   Unit test procedure
#
if __name__ == "__main__":
    entity = Entity()

# vim: set ts=4 sw=4 et
