#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

import unittest
import math
import pygame

__author__    = "Christofer Odén"
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
