#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
"""
Launches and initializes the game.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from argparse import ArgumentParser
from gameengine import gameengine
from vehicle import Vehicle
from missile import Missile

def initparse():
    parser = ArgumentParser(description=
            "The most awesomest game written by humans!")
    return parser

def main():
    parser = initparse()
    args = parser.parse_args()

    gameengine.initialize((800, 600))
    gameengine.add_entity(Vehicle((50, 200), 90))
    gameengine.add_entity(Vehicle((250, 200), 90))
    gameengine.add_entity(Missile((10, 10), 1, 45, "img/missile2.png", (32, 32), None))
    gameengine.start()

main()
