#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Initializes and starts the game client.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import os
from gameengine import gameengine
from vehicle import Vehicle
from missile import Missile

def main():
    print(os.path.abspath("."))
    gameengine.initialize((800, 600))
    gameengine.add_entity(Vehicle((50, 200), 90))
    gameengine.add_entity(Vehicle((250, 200), 90))
    gameengine.add_entity(Missile((10, 10), 1, 45, "client/img/missile2.png",
        (32, 32), None))
    gameengine.start()

main()

# vim: ts=4 et tw=79 cc=+1
