#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from socket import *
import logging
import select
import json
import zlib

class Server:
    """
    Handles transmission and receiving data, and keeps track of clients.

    """
    def __init__(self, port):
        self.addr = ('', port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clients = []

    def start(self):
        """Start the server."""
        self.sock.bind(self.addr)
        logging.info("Server listening on %s:%s." % self.addr)
        self.sock.listen(5)

    def get_input(self):
        """Read input from the network and return a list of it."""
        inputs = []
        read_list = [self.sock] + self.clients

        readable, writable, in_error = select.select(read_list, [], [], 0)
        for s in readable:
            if s is self.sock:
                client, addr = self.sock.accept()
                self.clients.append(client)
                logging.info("%s:%s connected." % addr)
            else:
                try:
                    data, addr = s.recvfrom(4096)
                    print("Input data '%s' from %s" % (data, addr))
                except IOError as e:
                    logging.info(e)
                    if e.errno == 104:
                        print("Removing client %s" % s)
                        self.clients.remove(s)
                    continue

                if data:
                    try:
                        inputs.append(json.loads(data))
                        print("Inputs: %s" % inputs)
                    except ValueError:
                        pass
                else:
                    print("Client %s disconnected." % s)
                    logging.info("Client disconnected.")
                    s.close()
                    self.clients.remove(s)

        return inputs

    def transmit(self, data):
        """Send the game state to all clients."""
        send_list = self.clients
        #msg = zlib.compress(json.dumps(data, separators=(',',':')))
        msg = json.dumps(data, separators=(',',':'))

        readable, writable, in_error = select.select([], send_list, [], 0)
        for s in writable:
            logging.debug("s: %s" % s)
            sent = s.send(msg)
            if not sent == len(msg):
                logging.error("Did not transmit all data")

# vim: ts=4 et tw=79 cc=+1
