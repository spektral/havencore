#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from socket import *
import logging
import select
import json

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
        self.sock.bind(self.addr)
        logging.info("Server listening on port %s:%s" % self.addr)
        self.sock.listen(5)

    def get_events(self):
        events = []
        read_list = [self.sock] + self.clients
        logging.debug("read_list: %s" % read_list)

        readable, writable, in_error = select.select(read_list, [], [], 0)
        for s in readable:
            if s is self.sock:
                client, addr = self.sock.accept()
                self.clients.append(client)
                logging.info("%s:%s connected" % addr)
            else:
                data = s.recv(4096)
                if data:
                    events += json.loads(data)
                else:
                    logging.info("%s:%s disconnected" % addr)
                    s.close()
                    self.clients.remove(s)

        return events

    def transmit(self, data):
        send_list = self.clients
        logging.debug("send_list: %s" % send_list)
        msg = json.dumps(data)

        readable, writable, in_error = select.select([], send_list, [], 0)
        for s in writable:
            logging.debug("s: %s" % s)
            sent = s.send(msg)
            if not sent == len(msg):
                logging.error("Did not transmit all data")
