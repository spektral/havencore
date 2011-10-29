#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from socket import *
import sys
import logging
import select
import json
import zlib
from pygame.event import Event
from pygame.locals import *
import gameengine
import vehicle

__author__    = "Christofer Odén"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

BUFSIZE = 65536

class Server:

    """
    Handles transmission and receiving data, and keeps track of clients.

    """

    use_compression = False

    def __init__(self, port):

        """Initialize the server"""

        self.logger = logging.getLogger('server.server.Server')

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

    def send(self, socket, data):

        """Pack and transmit data to a remote host"""

        if self.use_compression:
            try:
                data = zlib.compress(data)
            except:
                self.logger.error("Data could not be zlib compressed")
                self.logger.debug("Data causing error:\n%s" % data)
                return

        try:
            data = json.dumps(data, separators=(',',':'))
        except:
            self.logger.error("Data could not be JSON coded")
            self.logger.debug("Data causing error:\n%s" % data)
            return

        bytes_sent = socket.send(data)
        if not bytes_sent == len(data):
            self.logger.error("Could not send all data")

    def receive(self, socket):

        """Receive and unpack data from a remote host"""

        try:
            data = socket.recv(BUFSIZE)
        except IOError as e:
            # There might be an IOError which should not lead to disconnect.
            #if not e.errno == xxx:
            self.disconnect_client(socket, e)
            return (None, None)

        if not data:
            self.disconnect_client(socket, "Remote host disconnected")
            return (None, None)

        if self.use_compression == True:
            try:
                data = zlib.decompress(data)
            except:
                self.logger.error("Data could not be zlib decompressed")
                self.logger.debug("Data causing error:\n%s" % data)
                return (None, None)

        try:
            data = json.loads(data)
        except:
            self.logger.error("Data could not be JSON decoded")
            self.logger.debug("Data causing error:\n%s" % data)
            return (None, None)

        if not 'username' in data or not 'message' in data:
            self.logger.error("Data missing username or message")
            self.logger.debug("Data causing error:\n%s" % data)
            return (None, None)

        else:
            return (data['username'], data['message'])

    def on_connect(self):

        """Handle client(s) awaiting connection."""

        client_socket, address = self.server_socket.accept()

        username, message = self.receive(client_socket)

        if username in self.clients.keys():
            # The username is already taken, refuse connection
            self.send(client_socket, { 'accepted': False,
                                       'reason': 'Username unavailable' })
            self.logger.info("Refused connection from %s:%d, "
                    "username '%s' unavailable" %
                    (address[0], address[1], username))
            return False

        else:
            # The username is free, accept the client
            self.logger.info("Connection from %s:%d, username '%s' accepted" %
                    (address[0], address[1], username))
            self.send(client_socket, { 'accepted': True })
            self.clients[username] = client_socket

            # For now, create a vehicle:
            gameengine.gameengine.add_entity(vehicle.Vehicle(username, (400, 300), 120))

            return True

    def disconnect_client(self, socket, reason):
        s = None
        for username, s in self.clients.iteritems():
            if s == socket: break

        if not s:
            self.logger.debug("Could not delete and disconnect client socket")
            return

        s.close()
        del self.clients[username]
        self.logger.info("Disconnecting user '%s': %s" % (username, reason))

    def get_client_events(self, socket):

        """Parse all events from a single client, return a dict with
        username: events"""

        username, events = self.receive(socket)
        if None in (username, events):
            return (None, None)

        event_list = []

        for event in events:
            if 'type' not in event:
                self.logger.error("Malformed event")
                self.logger.debug("Event causing error:\n%s" % event)
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
                username, event_list = self.get_client_events(socket)
                if None in (username, event_list):
                    continue

                event_dict[username] = event_list

        return event_dict

    def transmit(self, data):

        """Send data to all clients."""

        send_list = self.clients.values()
        # Select only wriatable sockets.  Timeout = 0, instant
        readable, writable, in_error = select.select([], send_list, [], 0)
        for socket in writable:
            self.send(socket, data)

# vim: ts=4 et tw=79 cc=+1
