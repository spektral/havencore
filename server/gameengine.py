#!/usr/bin/python2
# -*- coding: utf-8 -*-

import logging
import pygame
from pygame.locals import *
from server import Server 

__author__    = "Christofer Odén"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

class GameEngine(object):

    """Server-side class responsible for the main game loop.

    Public methods:

    initialize -- Initialize the server.  Take the port to listen on
    as argument.

    start -- Start the main game loop and begin listening for client
    connections.

    add_entity -- Append an object to the entity list.  Take the object
    to append as argument.


    Other methods of interest:

    handle_input -- Handle to network input, collisions and other
    events that set the manner in which the update is going to run.

    update -- Perform game logic like moving and damaging objects,
    react to events handled by handle_input.

    handle_output -- Send all updates to the game state to the
    connected peers.

    """

    def initialize(self, port):

        """Create the server object and an empty entity list."""

        self.logger = logging.getLogger('server.gameengine.GameEngine')
        self.logger.info("Initializing server engine...")

        self.server = Server(port)

        self.entities = []

    def add_entity(self, entity):

        """Append the entity to the entity list."""

        self.entities.append(entity)

    def start(self):

        """Start the game loop and start listening for clients"""

        self.logger.info("Starting server engine...")

        self.server.listen()

        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            self.handle_output()
            self.fps_clock.tick(50)

    def quit(self):

        """Break the main game loop."""

        self.logger.info("Quitting server engine...")

        self.is_running = False

    def handle_input(self):

        """Propagate network input and handle collisions."""

        for player, events in self.server.get_events().iteritems():
            for entity in filter(lambda x:x.player == player, self.entities):
                for event in events:
                    entity.handle_input(event)

        for entity in self.entities:
            entity.check_collisions(self.entities)

    def update(self):

        """Weed out dead entities and update the rest."""

        self.entities = filter(lambda x:x.alive, self.entities)

        for entity in self.entities:
            entity.update()

    def handle_output(self):
        """Transmit the game state to the clients."""
        net_package = [x.get_state() for x in self.entities]
        self.server.transmit(net_package)

    def __repr__(self):
        return self.entities



gameengine = GameEngine()

# vim: ts=4 et tw=79 cc=+1
