#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""This module handles terrain data, such as reading it from a database
and presenting an interface to access it from other classes"""

import logging
from random import randint
from graphics import *

__author__    = "Christofer Odén"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

class TerrainData:

    """Handles the terrain data"""

    def __init__(self, filename, spritemap):

        """Read terrain data from file"""

        self.logger = logging.getLogger('client.terraindata.TerrainData')
        self.sprite = SpriteArray(spritemap)

        infile = open(filename, "r")

        self.w = int(infile.readline())
        self.h = int(infile.readline())

        self.tiles = []
        for i in range(self.w):
            self.tiles.append([[]] * self.h)
        self.logger.debug(self.tiles)

        for y in range(self.h):
            for x in range(self.w):
                self.logger.debug("(%d,%d)" % (x, y))
                self.tiles[x][y] = int(infile.read(1))
            assert(infile.read(1) == '\n')

    def draw(self, (x, y), tile_x, tile_y):

        """Draw tiles at the right coordinates"""

        screen = display.get_surface()
        tile = self.tiles[tile_x][tile_y]
        self.sprite.draw(screen, x, y)


def create_random_terrain():

    """Creates a simple random map"""

    outfile = open("client/data/terraindata.map", "w")

    width = 200
    height = 200
    outfile.write("%d\n" % width)
    outfile.write("%d\n" % height)
    for row in range(height):
        for col in range(width):
            outfile.write("%d" % randint(0,3))
        outfile.write('\n')
