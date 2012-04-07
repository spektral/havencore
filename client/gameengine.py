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

from entitylist import entity_container
from entitylist import *

import graphics
from graphics import spritemaps

from jukebox import jukebox

from terraindata import TerrainData

from hud import hud

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

        """Initialize connection data"""

        self.logger = logging.getLogger('client.gameengine.Connection')

        self.username = username

        self.addr = addr

    def connect(self):

        """Negotiate for connection to remote host."""

        self.logger.info("Connecting to %s:%s." % self.addr)

        try:
            self.socket = create_connection(self.addr, 5)
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
        try: 
            for socket in readable:
                servername, state = net.receive(self.socket)
        except ValueError:
            self.logger.error("gameengine.get_state: ValueError")
            state = None

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

        """Initialize the game engine.
        
        Set up the main window, initialize a connection to a server and
        initialize the base objects."""

        self.logger = logging.getLogger('client.gameengine.GameEngine')
        self.logger.info("Initializing client engine...")

        self.logger.info("Initializing pygame...")
        pygame.init()

        modes = pygame.display.list_modes()
        self.screen = pygame.display.set_mode(modes[1])
        pygame.display.set_caption("Haven Core")

        self.username = username
        self.connection = Connection(username, addr)

        graphics.load_sprites()

        self.terrain_data = TerrainData('client/data/terraindata.map',
                                        spritemaps['terrain'])

        self.entities = entity_container

        self.hud = hud()

        jukebox.initialize()

    def start(self):

        """Start the game engine.
        
        Establish the server connection, start the frame timer and
        launch the main game loop."""

        self.logger.info("Starting client engine...")
        self.connection.connect()
        self.fps_clock = pygame.time.Clock()

        self.is_running = True
        while(self.is_running):
            self.handle_events()
            self.update()
            self.draw()
            self.fps_clock.tick(50)
        pygame.quit()

    def quit(self):

        """Stop the game loop."""

        self.logger.info("Stopping client engine...")
        self.is_running = False
    
    def handle_events(self):

        """Send user input to the server and handle client side events."""

        events = []

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                    break

            self.entities.handle_event(event)

            if event.type in (KEYDOWN, KEYUP):
                events.append({ 'type': event.type, 'key': event.key })
            
            if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                events.append({ 'type': event.type,
                                'button': event.button,
                                'pos': event.pos })
                self.logger.debug(repr(events[-1]))

        events.append({ 'type': MOUSEMOTION, 'pos': pygame.mouse.get_pos() })

        # Only bother to transmit events that matter
        if events:
            self.connection.transmit({ 'label': 'events', 'events': events })

    def update(self):

        """Perform client side logic and fetch updates from server."""

        self.get_server_state()

        vehicles = self.entities.get_all_vehicles()
        self.hud.update(vehicles, self.username)

    def get_server_state(self):

        """Get state from server and update accordingly."""

        state_list = self.connection.get_state()
        #self.logger.debug("State List: %s" % state_list)

        for state in state_list:
            for entity in state:
                #self.logger.debug("State: %s" % state)
                name = entity['name']
                dict = entity['dict']
                serial = dict['serial']

                entity = self.entities.get_with_serial(serial, layer=SERVER)

                # Create objects that doesn't exist yet
                if not entity:
                    if name == 'Vehicle':
                        self.entities.append(SERVER,
                                Vehicle(dict, spritemaps['vehicle']))

                    if name in ('Rocket', 'HomingMissile'):
                        self.entities.append(SERVER,
                                Missile(dict, spritemaps['missile']))
                        jukebox.play_sound('rocket')

                    if name == 'MgBullet':
                        self.entities.append(SERVER,
                                Machinegun(dict))

                    if name == 'LandMine':
                        self.entities.append(SERVER,
                                LandMine(dict))

                    if name == 'Block':
                        pass
                        #print "Block"
                   #     self.mapHandler.change_color_at(

                # If the object exists, update it with the new data
                else:
                    entity.__dict__.update(dict)

        self.entities.update()

        jukebox.update()

        self.entities.clean_dead()

    def draw(self):

        """Draw stuff to the screen."""

        self.screen.fill((0, 0, 50))
        self.entities.draw()
        self.hud.draw()

        pygame.display.update()

    def __repr__(self):
        return self.entities


gameengine = GameEngine()

# vim: ts=4 et tw=79 cc=+1
