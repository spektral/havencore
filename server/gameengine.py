#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

import sys
import logging

import select
from socket import *
import errno

import pygame
from pygame.event import Event
from pygame.locals import *

from common import net

__author__    = "Christofer Odén"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

class Server:

    """
    Handles transmission and receiving data, and keeps track of clients.

    """

    def __init__(self, port):

        """Initialize the server"""

        self.logger = logging.getLogger('server.gameengine.Server')

        self.port = port

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.clients = {}

    def listen(self):

        """Start to listen for connections"""

        try:
            self.server_socket.bind(('', self.port))
        except OverflowError as e:
            self.logger.critical("Bind to port %d failed: %s" %
                    (self.port, e.message))
            sys.exit(1)

        self.logger.info("Starting to listen on %s" % self.port)
        self.server_socket.listen(5)

    def on_connect(self):

        """Handle client(s) awaiting connection."""

        client, address = self.server_socket.accept()

        try:
            username, messages = net.receive(client)
        except IOError as e:
            if e.errno == errno.ECONNRESET:
                self.disconnect_client(client, "Connection lost")
            else:
                self.logger.error(e.strerror)
            return

        if username in self.clients.keys():
            # The username is already taken, refuse connection
            self.logger.info("Refused connection from %s:%d, "
                    "username '%s' unavailable" %
                    (address, username))

            net.send(client, { 'accepted': False,
                               'reason': 'Username unavailable' })

            self.disconnect_client(client, "Username unavailable")

            return False

        else:
            # The username is free, accept the client
            self.logger.info("Connection from %s:%d, username '%s' accepted" %
                    (address[0], address[1], username))

            net.send(client, { 'accepted': True })
            self.clients[username] = client

            # For now, create a vehicle:
            gameengine.add_entity(Vehicle(username, (400, 300),
            120,('bigmotor','smallmotor')))

            return True

    def disconnect_client(self, socket, reason):
        for username, client in self.clients.iteritems():
            if client == socket: break

        if not client:
            self.logger.debug("Could not delete and disconnect client socket")
            return

        client.close()
        del self.clients[username]
        self.logger.info("Disconnecting user '%s': %s" % (username, reason))

    def get_client_events(self, socket):

        """Parse all events from a single client, return a dict with
        username: events"""

        try:
            username, messages = net.receive(socket)
            if username == None:
                return
        except IOError as e:
            if e.errno == errno.ECONNRESET:
                self.disconnect_client(socket, "Connection lost")
            else:
                self.logger.error(e.strerror)
            return None, None

        events = []
        for message in filter(lambda m:m['label'] == 'events', messages):
            events += message['events']

        #self.logger.debug("Events: %s" % events)

        event_list = []
        for event in events:
            #self.logger.debug("Event: %s" % event)
            if 'type' not in event:
                self.logger.error("Malformed event")
                self.logger.debug("Event causing error:\n%s" % event)
                raise Exception("Malformed event")
                return username, None

            elif event['type'] in (KEYDOWN, KEYUP):
                event = Event(event['type'], { 'key': event['key'] })

            elif event['type'] in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                event = Event(event['type'], { 'button': event['button'],
                                               'pos': event['pos'] })

            event_list.append(event)

        return username, event_list

    def get_events(self):

        """Handle messages from the network and return a dict with an input
        list for each player."""

        event_dict = {}

        read_list = [self.server_socket] + list(self.clients.values())
        # Select only readable sockets.  Timeout = 0, instant
        readable, writable, in_error = select.select(read_list, [], [], 0)
        for socket in readable:

            if socket is self.server_socket:
                # New client wants to connect
                self.on_connect()

            else:
                # There are new messages from connected clients
                username, events = self.get_client_events(socket)
                if not events:
                    continue

                event_dict[username] = events

        return event_dict

    def transmit(self, data):

        """Send data to all clients."""

        send_list = self.clients.values()
        # Select only wriatable sockets.  Timeout = 0, instant
        readable, writable, in_error = select.select([], send_list, [], 0)
        for socket in writable:
            net.send(socket, data)


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

from entities import *

# vim: ts=4 et tw=79 cc=+1
