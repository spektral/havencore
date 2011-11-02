#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

#author: björn nordström

from entities import Vehicle
import pygame
from defines import *
class HUD:
    def __init__(self, (x,y),vehicle = None):
        # start pos of HUD
        self.pos = (x,y)
        self.rect = pygame.Rect(x,y,600,100)
        if vehicle == None:
            self.health = 100
        else:
            self.health = vehicle.get_health()
    def update(self):
        pass

    def draw_frame(self,screen):
        #pygame.draw.line(screen,black, self.pos, (self.pos[0]+WIDTH,   self.pos[1]), 10)
        pygame.draw.rect(screen,black, self.rect)
    def draw_hp_circle(self, screen):
        pygame.draw.circle(screen, red, (self.pos[0]+100,self.pos[1]+50), 50, 0)
        
    def draw(self,screen):
        self.draw_frame(screen)
        self.draw_hp_circle(screen)

# vim: ts=4 et tw=79 cc=+1
