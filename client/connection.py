#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from socket import *
import sys
import logging
import select
import json
import zlib

__author__    = "Christofer Odén"
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

BUFSIZE = 65536

class Connection:

    """
    Handles transmission and receiving data to the server.

    """

    use_compression = False

    def __init__(self, username, addr):

        """Initialize the server"""

        self.logger = logging.getLogger('client.connection.Connection')

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

        self.logger.debug("Server response to connect: %s" % response)
        if response['accepted'] == False:
            self.logger.critical("Connection failed: %s" % response['reason'])
        else:
            self.logger.info("Connected")

    def send(self, data):

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

        bytes_sent = self.socket.send(data)
        if not bytes_sent == len(data):
            self.logger.error("Could not send all data")

    def receive(self):

        """Receive and unpack data from a remote host"""

        try:
            data = self.socket.recv(BUFSIZE)
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

# vim: ts=4 et tw=79 cc=+1
