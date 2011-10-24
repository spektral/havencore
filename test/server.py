#!/usr/bin/python2

import socket
import select
import sys

class Listener:
    def __init__(self, port):
        self.events = []
        self.peers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(0)
        self.socket.bind(('', port))

    def receive(self):
        read_list = [self.socket]
        readable, writable, in_error = select.select(read_list, [], [], 0)
        if readable:
            s = readable[0]

            while True:
                # Parse the data
                try:
                    data, addr = s.recvfrom(1024)
                except socket.error as e:
                    if e.errno == 11:
                        break

                fields = data.split('|')

                if not len(fields) == 3:
                    sys.stderr.write("Malformed packet: %s" % data)

                # Begin constructing the event object
                event = {}
                try:
                    event['id'] = { 'name': fields[0],
                            'addr': addr }
                    event['type'] = fields[1]
                    event['data'] = fields[2]
                except IndexError:
                    sys.stderr.write("Malformed packet: %s" % data)

                if not event['id']['name'] in self.peers:
                    self.peers[event['id']['name']] = event['id']['addr']

                self.events.append(event)

    def broadcast(self, data):
        for peer in self.peers.values():
            self.socket.sendto(str(data), peer)



#
#   Unit test procedure
#
if __name__ == "__main__":
    listener = Listener(60000)
    while True:
        listener.receive()
        while listener.events:
            listener.broadcast(listener.events.pop(0))
