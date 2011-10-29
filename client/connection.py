#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from socket import *
import logging
import select
import json
import zlib

class Connection:

    """
    Handles transmission and receiving data to the server.

    """

    def __init__(self, addr):
        self.addr = addr
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def establish(self):
        """Start the server."""
        logging.info("Connecting to %s:%s." % self.addr)
        self.sock.connect(self.addr)

    def get_server_state(self):
        """Read server state return a representation of it."""
        state = []
        read_list = [self.sock]

        readable, writable, in_error = select.select(read_list, [], [], 0)
        for s in readable:
            data, addr = s.recvfrom(4096)
            if data:
                try:
                    #state = zlib.decompress(json.loads(data))
                    state = json.loads(data)
                except ValueError:
                    pass
            else:
                logging.error("Connection lost.")
                s.close()

        return state

    def transmit(self, data):
        """Send the game state to all clients."""
        send_list = [self.sock]
        #msg = zlib.compress(json.dumps(data, separators=(',',':')))
        msg = json.dumps(data, separators=(',',':'))

        readable, writable, in_error = select.select([], send_list, [], 0)
        for s in writable:
            logging.debug("s: %s" % s)
            sent = s.send(msg)
            if not sent == len(msg):
                logging.error("Did not transmit all data")

# vim: ts=4 et tw=79 cc=+1
