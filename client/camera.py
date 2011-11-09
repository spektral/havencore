#!/usr/bin/python -tt
# -*- coding: utf-8 -*-


import pygame
from pygame import display
from pygame.locals import *

from entities import *


class Camera:

    def __init__(self):
        Rect self.rcWin((0,0),(display.get_size()))

    def assign_terrain(self, terrain):
        pass

    def assign_entity(self, player_ent):
        self.player_ent = player_ent

    def update(self, ents):
        self.rcWin.x = player_ent.x - ( self.rcWin.w / 2 )
        self.rcWin.y = player_ent.y - ( self.rcWin.h / 2 )
        
        self.ents = ents

    def draw(self):
        screen = display.get_surface()
        
        for e in self.ents:
            if e['name'] == 'TerrainData':
                for tiley in range(self.rcWin.y, self.rcWin.h):
                    for tilex in range(self.rcWin.x, self.rcWin.w):
                        e.draw((self.rcWin.x, self.rcWin.y), tilex, tiley)

            elif e.x >= self.rcWin.x && e.x <= self.rcWin.w:
                if e.y >= self.rcWin.y && e.y <= self.rcWin.h:
                    e.draw((e.x - self.rcWin.x), (e.y - self.rcWin.y))


if __name__ == "__main__":
    print "test"

