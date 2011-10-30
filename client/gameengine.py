#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
This class links the user interface to the game objects and drives the
game loop.

"""

import sys
import logging

import json
import zlib

import select
from socket import *

import pygame
from pygame.locals import *

from entities import *

from defines import *
from jukebox import JukeBox
from mapHandler import MapHandler

__author__    = "Gustav Fahlén, Christofer Odén, Max Sidenstjärna"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"


class Connection:

    """
    Handles transmission and receiving data to the server.

    """

    BUFSIZE = 65536
    use_compression = True

    def __init__(self, username, addr):

        """Initialize the server"""

        self.logger = logging.getLogger('client.gameengine.Connection')

        self.username = username

        self.addr = addr
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def connect(self):

        """Connect to the remote host"""

        self.logger.info("Connecting to %s:%s." % self.addr)

        try:
            self.socket.connect(self.addr)
        except IOError as e:
            self.logger.critical("Connection failed: %s" % e)
            sys.exit(1)

        self.send({'username': self.username, 'message': 'ICANHAZCONNECT?'})

        response = self.receive()
        if 'accepted' not in response:
            self.logger.critical("Bad server response")
            self.logger.debug("Data causing error:\n%s" % response)
            sys.exit(1)

        if response['accepted'] == False:
            self.logger.critical("Connection failed: %s" % response['reason'])
        else:
            self.logger.info("Connected")

    def send(self, data):

        """Pack and transmit data to a remote host"""

        try:
            data = json.dumps(data, separators=(',',':'))
        except:
            self.logger.error("Data could not be JSON coded")
            self.logger.debug("Data causing error:\n%s" % data)
            return

        if self.use_compression:
            try:
                data = zlib.compress(data)
            except:
                self.logger.error("Data could not be zlib compressed")
                self.logger.debug("Data causing error:\n%s" % data)
                return

        bytes_sent = self.socket.send(data)
        if not bytes_sent == len(data):
            self.logger.error("Could not send all data")

    def receive(self):

        """Receive and unpack data from a remote host"""

        try:
            data = self.socket.recv(self.BUFSIZE)
        except IOError as e:
            # There might be an IOError which should not lead to disconnect.
            #if not e.errno == xxx:
            self.logger.critical("Error receiving data: %s" % e)
            sys.exit(1)

        if not data:
            self.logger.critical("Remote host disconnected")
            sys.exit(1)

        if self.use_compression == True:
            try:
                data = zlib.decompress(data)
            except:
                self.logger.error("Data could not be zlib decompressed")
                self.logger.debug("Data causing error:\n%s" % data)
                return None

        try:
            data = json.loads(data)
        except:
            self.logger.error("Data could not be JSON decoded")
            self.logger.debug("Data causing error:\n%s" % data)
            return None

        else:
            return data

    def get_state(self):

        """Parse server state messages and return a list of it"""

        state = []

        read_list = [self.socket]
        readable, writable, in_error = select.select(read_list, [], [], 0)
        for socket in readable:
            state = self.receive()

        if state == None:
            return []
        else:
            return state

    def transmit(self, data):

        """Send the game state to all clients."""

        send_list = [self.socket]
        readable, writable, in_error = select.select([], send_list, [], 0)
        for socket in writable:
            self.send(data)


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
        self.connection = Connection(username, addr)
        self.mapHandler = MapHandler(WIDTH, HEIGHT, 40)
        self.jukebox = JukeBox()
        self.entities = []

    def add_entity(self, entity):
        """Append a game object to the object list."""
        self.entities.append(entity)

    def start(self):
        """Start the game engine."""
        logging.info("Starting client engine...")
        self.connection.connect()
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

        event_pack = { 'username': self.username, 'message': [] }

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
                event_pack['message'].append(net_event)

        if event_pack['message']:
            self.connection.transmit(event_pack)
            
            #for entity in self.entities:
            #    entity.handle_input(event)
            #    self.mapHandler.handle_input(event)

        #for entity in self.entities:
        #    entity.check_collisions(self.entities)

    def get_server_state(self):

        """Get state from server and update the known entities."""

        state = self.connection.get_state()
        if state:
            self.entities = []

            for input in state:
                name = input['name']
                dict = input['dict']
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

                # If the object doesn't exist, update it with the new data
                else:
                    entity = filter(lambda x:x.serial == serial,
                                    self.entities)[0]
                    entity.__dict__.update(dict)

        for entity in self.entities:
            entity.update()

        self.jukebox.update()

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
