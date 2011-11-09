#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""A system for providing visual status feedback to the player"""

__author__   = "Björn Nordström, Christofer Odén"
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from pygame import display, Rect, draw, font

class Bar:

    """A bar displaying a ratio of something"""

    def __init__(self, rect, max_val, color):
        self.rect = rect
        self.max_val = float(max_val)
        self.color = color
        self.ratio = 1.0

    def update(self, val):
        self.ratio = val / self.max_val

    def draw(self):
        screen = display.get_surface()

        draw.rect(screen, (50, 50, 50), self.rect, 0)

        width = self.ratio * self.rect.w
        bar_rect = Rect(self.rect.x + 2, self.rect.y + 2,
                width - 4, self.rect.h - 4)
        draw.rect(screen, self.color, bar_rect)

class NamePlates:

    """ Nameplates for the vehicles  """
    
    def __init__(self):
        self.vehicles = {}
        self.fonts = font.SysFont("none", 20)
       
    def update(self, entity):
        for vehicle in entity:
            self.vehicles[vehicle.player] = (int(vehicle.x - 15), int(vehicle.y - 70))
    def draw(self):
        screen = display.get_surface()
        for name in self.vehicles.keys():
            text = self.fonts.render(name, 1, (255,255,0))
            screen.blit(text, self.vehicles[name])
         

class hud:

    """Heads Up Display

    Shows the player health on the screen"""

    def __init__(self):
        
        screen_w, screen_h = display.get_surface().get_size()
        self.health_bar = Bar(
                Rect(10, screen_h - 20, 300, 10), 100, (200, 0, 0))
        self.name_plates = NamePlates()

    def update(self, entities, username):
        if (entities):
            for vehicle in entities:
                if vehicle.player == username:
                    self.health_bar.update(vehicle.health)
            
            self.name_plates.update(entities)
        else:
            self.health_bar.update(0)
        
    def draw(self):
        self.health_bar.draw()
        self.name_plates.draw()

# vim: ts=4 et tw=79 cc=+1
