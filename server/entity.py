#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import unittest
import pygame
import math

class Entity(object):

    """Abstract base class for data belonging to all kinds of of game
    objects."""

    ticker = 0

    def __init__(self, player, (x, y), r):
        self.serial = Entity.ticker
        Entity.ticker += 1
        self.player = player
        self.x = x
        self.y = y
        self.r = r
        self.collision_list = []
        self.is_collidable = True
        self.alive = True

    def get_state(self):
        """Return a dictionary representation of the instance."""
        return { 'type': 'entity',
                 'name': self.__class__.__name__,
                 'dict': self.__dict__ }

    def check_collisions(self, entities):
        for entity in entities:
            if entity is not self and entity.is_collidable:
                dx = entity.x - self.x
                dy = entity.y - self.y
                rr = (entity.r + self.r) / 2
                if dx * dx + dy * dy < rr * rr:
                    self.collision_list.append(entity)


class Test(unittest.TestCase):
    def setUp(self):
        self.entities = []
        self.entities.append(Entity('0', (0, 0), 20))
        self.entities.append(Entity('1', (0, 0), 20))
        self.entities.append(Entity('2', (0, 0), 20))

    def test_serial(self):
        self.assertEqual(self.entities[0].serial, 0)
        self.assertEqual(self.entities[1].serial, 1)
        self.assertEqual(self.entities[2].serial, 2)
        self.assertEqual(Entity.ticker, 3)

if __name__ == "__main__":
    unittest.main()

# vim: ts=4 et tw=79 cc=+1
