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
import connection
from vehicle import Vehicle
from missile import Missile

class GameEngine(object):

    """
    Main class for the client side.  Keep track of common data.

    This class should know about all the objects in the game, and tell
    them to do stuff with each other.  It should not do anything real
    itself, but delegate to and command other objects.
    
    """

    def initialize(self, username, addr):
        """Initialize the game engine with screen resolution."""
        logging.info("Initializing client engine...")

        logging.info("Initializing pygame...")
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Haven Core")

        self.username = username
        self.connection = connection.Connection(addr)
        self.mapHandler = MapHandler(WIDTH, HEIGHT, 40)
        self.jukebox = JukeBox()
        self.entities = []

    def add_entity(self, entity):
        """Append a game object to the object list."""
        self.entities.append(entity)

    def start(self):
        """Start the game engine."""
        logging.info("Starting client engine...")
        self.connection.establish()
        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.get_server_state()
            self.draw()
            self.fps_clock.tick(50)

    def quit(self):
        logging.info("Stopping client engine...")
        self.is_running = False
    
    def handle_input(self):

        """Take input from the user and check for other events like
        collisions."""

        event_pack = { 'player': self.username, 'events': [] }

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                    break

            net_event = { 'type': event.type }

            if event.type in (KEYDOWN, KEYUP):
                net_event['key'] = event.key
                event_pack['events'].append(net_event)

        logging.debug("Event package: %s" % event_pack)
        if event_pack['events']:
            self.connection.transmit(event_pack)
            
            #for entity in self.entities:
            #    entity.handle_input(event)
            #    self.mapHandler.handle_input(event)

        #for entity in self.entities:
        #    entity.check_collisions(self.entities)

    def get_server_state(self):

        """Get state from server and update the known entities."""

        state = self.connection.get_server_state()
        print("Received: %s" % state)

        for input in state:
            serial = input['dict']['serial']
            name = input['name']
            dict = input['dict']

            # Create objects that doesn't exist yet
            if (serial not in [s.serial for s in self.entities]):

                if name == 'Vehicle':
                    self.entities.append(
                            Vehicle(dict, "client/img/crawler_sprites.png",
                                (128, 128)))

                if name == 'Missile':
                    self.entities.append(
                            Missile(dict, "client/img/missile2.png", (32, 32)))

            # If the object doesn't exist, update it with the new data
            else:
                entity = filter(lambda x:x.serial == serial, self.entities)[0]
                entity.__dict__.update(dict)

        for entity in self.entities:
            entity.update()

        self.jukebox.update()

        self.entities = filter(lambda x:x.alive, self.entities)
        print("%s.entities: %s" % (self.__class__.__name__, self.entities))

    def draw(self):
        """Draw stuff to the screen."""
        self.screen.fill((66, 66, 111))
        self.mapHandler.draw(self.screen)

        for entity in self.entities:
            print(entity)
            entity.draw(self.screen)

        pygame.display.update()

    def __repr__(self):
        return self.entities

gameengine = GameEngine()

# vim: ts=4 et tw=79 cc=+1
