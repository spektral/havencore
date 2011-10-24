#!/usr/bin/python2 -tt

import socket

class Sender:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_msg(self, data):
        self.socket.sendto("%s|%s|%s" % (self.name, "msg", data), ('127.0.0.1', self.port))



#
#   Unit test procedure
#
if __name__ == "__main__":
    sender = Sender('spektre', 60000)
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    sender.send_msg("Hello")
    sender.send_msg("World!")
    while True:
        sender.socket.setblocking(0)
        try:
            answer = sender.socket.recvfrom(1024)
            print(answer)
        except socket.error:
            pass
