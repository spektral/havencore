#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
This class links the user interface to the game objects and drives the
game loop.

"""

import sys
import logging

import select
from socket import *

import pygame
from pygame.locals import *

from common import net

from entities import *

from defines import *
from jukebox import jukebox
from mapHandler import MapHandler

__author__    = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"


class Connection:

    """
    Handle communication between server and client.

    Perform connect, send events, and receive state.

    """

    def __init__(self, username, addr):

        """Initialize the server"""

        self.logger = logging.getLogger('client.gameengine.Connection')

        self.username = username

        self.addr = addr
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def connect(self):

        """Negotiate for connection to remote host."""

        self.logger.info("Connecting to %s:%s." % self.addr)

        try:
            self.socket.connect(self.addr, 5)
        except IOError as e:
            self.logger.critical("Connection failed: %s" % e)
            sys.exit(1)

        net.send(self.socket, 'icanhazconnectplz?', self.username)

        servername, response = net.receive(self.socket)
        if servername == None:
            self.logger.critical("Connection failed: Unknown reason")

        if 'accepted' not in response[0]:
            self.logger.critical("Bad server response")
            self.logger.debug("Data causing error:\n%s" % response)
            sys.exit(1)

        if response[0]['accepted'] == False:
            self.logger.critical("Connection failed: %s" %
                                 response[0]['reason'])
        else:
            self.logger.info("Connected")

    def get_state(self):

        """Parse server state messages and return a list of it"""

        state = []

        read_list = [self.socket]
        readable, writable, in_error = select.select(read_list, [], [], 0)
        for socket in readable:
            servername, state = net.receive(self.socket)

        if state == None:
            return []
        else:
            return state

    def transmit(self, message):

        """Send the game state to all clients."""

        send_list = [self.socket]
        readable, writable, in_error = select.select([], send_list, [], 0)
        for socket in writable:
            net.send(socket, message, self.username)


class GameEngine(object):

    """
    Main class for the client side.  Keep track of common data.

    This class should know about all the objects in the game, and tell
    them to do stuff with each other.  It should not do anything real
    itself, but delegate to and command other objects.
    
    """

    def initialize(self, username, addr):
        """Initialize the game engine with screen resolution."""
        self.logger = logging.getLogger('client.gameengine.GameEngine')
        self.logger.info("Initializing client engine...")

        self.logger.info("Initializing pygame...")
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Haven Core")

        jukebox.initialize()

        self.username = username
        self.connection = Connection(username, addr)
        self.mapHandler = MapHandler(WIDTH, HEIGHT, 40)
        self.entities = []

    def add_entity(self, entity):
        """Append a game object to the object list."""
        self.entities.append(entity)

    def start(self):
        """Start the game engine."""
        self.logger.info("Starting client engine...")
        self.connection.connect()
        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.get_server_state()
            self.draw()
            self.fps_clock.tick(50)

    def quit(self):
        self.logger.info("Stopping client engine...")
        self.is_running = False
    
    def handle_input(self):

        """Take input from the user and check for other events like
        collisions."""

        events = []

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                    break

            if event.type in (KEYDOWN, KEYUP):
                events.append({ 'type': event.type, 'key': event.key })

        # Only bother to transmit events that matter
        if events:
            self.connection.transmit({ 'label': 'events', 'events': events })
            
            #for entity in self.entities:
            #    entity.handle_input(event)
            #    self.mapHandler.handle_input(event)

        #for entity in self.entities:
        #    entity.check_collisions(self.entities)

    def get_server_state(self):

        """Get state from server and update the known entities."""

        state_list = self.connection.get_state()
        #self.logger.debug("State List: %s" % state_list)
        #if state_list:
            #self.entities = []

        for state in state_list:
            for entity in state:
                #self.logger.debug("State: %s" % state)
                name = entity['name']
                dict = entity['dict']
                serial = dict['serial']

                # Create objects that doesn't exist yet
                if (serial not in [s.serial for s in self.entities]):

                    if name == 'Vehicle':
                        self.entities.append(
                                Vehicle(dict, "client/img/crawler_sprites.png",
                                    (128, 128)))

                    if name == 'Missile':
                        self.entities.append(
                                Missile(dict, "client/img/missile2.png",
                                        (32, 32)))
                        jukebox.play_sound('rocket')

                # If the object exists, update it with the new data
                else:
                    entity = filter(lambda x:x.serial == serial,
                                    self.entities)[0]
                    entity.__dict__.update(dict)

        for entity in self.entities:
            entity.update()

        jukebox.update()

        self.entities = filter(lambda x:x.alive, self.entities)

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
