#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
This class links the user interface to the game objects and drives the
game loop.

"""

__author__    = "Christofer Odén"
__email__     = "bei.oden@gmail.com"
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import pygame
from pygame.locals import *
import entity
import missile
import vehicle
import explode

class GameEngine:
    """
    Game engine is implemented according to the "Borg" pattern.  All instances
    share the same data.
    
    """

    entities = []

    def __init__(self):
        pass

    def initialize(self, screen_res):
        print "Initializing pygame..."
        pygame.init()

        self.screen = pygame.display.set_mode(screen_res)
        pygame.display.set_caption("pybattle")

        self.fps_clock = pygame.time.Clock()

        self.entities.append(vehicle.Vehicle(200, 200, 90))
        self.entities.append(missile.Missile(10, 10, 1, 45))
        print("Entities: %s" % self.entities)

    def get_entities(self):
        return getattr(self, 'entities', None)

    def start(self):
        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            #self.collide_detect()
            self.draw()
            self.fps_clock.tick(50)

    def quit(self):
        self.is_running = False
    
    # Better name "handle_events"
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                    break

            for entity in self.entities:
                entity.handle_input(event)

        for entity in self.entities:
            entity.check_collisions(self.entities)

    def update(self):
        for entity in self.entities:
            entity.update()

        self.entities = [e for e in self.entities if e.alive == True]

    def draw(self):
        self.screen.fill(pygame.Color(66, 66, 111))

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.update()
        print(self.entities)

    def __repr__(self):
        return self.entities

if __name__ == "__main__":
    game_engine = GameEngine()
    game_engine.initialize((640, 480))
    game_engine.start()
