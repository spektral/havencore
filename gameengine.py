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
from defines import *
from jukebox import JukeBox
from mapHandler import MapHandler
class GameEngine(object):
    """
    Game engine is implemented according to the "Borg" pattern.  All instances
    share the same data.
    
    """
    def initialize(self, screen_res):
        print "Initializing pygame..."
        pygame.init()
        self.mapHandler = MapHandler(WIDTH,HEIGHT,40)
        self.entities = []
        self.JukeBox = JukeBox()

        print "Setting up video mode..."
        self.screen = pygame.display.set_mode(screen_res)
        pygame.display.set_caption("pybattle")

    def add_entity(self, entity):
        self.entities.append(entity)

    def start(self):
        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            self.draw()
            self.JukeBox.timeToChangeSong()
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
                self.mapHandler.handle_input(event)

        for entity in self.entities:
            entity.check_collisions(self.entities)

    def update(self):
        for entity in self.entities:
            entity.update()

        self.entities = [e for e in self.entities if e.alive == True]

    def draw(self):
        self.screen.fill((66, 66, 111))
        self.mapHandler.draw(self.screen)
        

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.update()

    def __repr__(self):
        return self.entities



gameengine = GameEngine()
