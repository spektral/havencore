#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
This class links the user interface to the game objects and drives the
game loop.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import logging
import pygame
from pygame.locals import *
from defines import *
from jukebox import JukeBox
from mapHandler import MapHandler

class GameEngine(object):

    """
    Main class for the client side.  Keep track of common data.

    This class should know about all the objects in the game, and tell
    them to do stuff with each other.  It should not do anything real
    itself, but delegate to and command other objects.
    
    """

    def initialize(self, port):
        """Initialize the game engine with screen resolution."""
        logging.getLogger(__name__)
        logging.info("Initializing client engine...")
        logging.info("Initializing pygame...")
        pygame.init()
        self.mapHandler = MapHandler(WIDTH,HEIGHT,40)
        self.entities = []
        self.jukebox = JukeBox()

        logging.info("Setting up video mode...")
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("pybattle")

    def add_entity(self, entity):
        """Append a game object to the object list."""
        self.entities.append(entity)

    def start(self):
        """Start the game engine."""
        logging.info("Starting client engine...")
        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            self.draw()
            self.fps_clock.tick(50)

    def quit(self):
        logging.info("Stopping client engine...")
        self.is_running = False
    
    # Better name "handle_events"
    def handle_input(self):
        """Take input from the user and check for other events like
        collisions."""
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
        """Tell all objects to perform their logic. Weed out dead
        objects."""
        for entity in self.entities:
            entity.update()

        self.jukebox.update()

        self.entities = [e for e in self.entities if e.alive == True]

    def draw(self):
        """Draw stuff to the screen."""
        self.screen.fill((66, 66, 111))
        self.mapHandler.draw(self.screen)

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.update()

    def __repr__(self):
        return self.entities

gameengine = GameEngine()

# vim: ts=4 et tw=79 cc=+1
