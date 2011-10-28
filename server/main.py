#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Launches and initializes the game.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from argparse import ArgumentParser
import logging
from vehicle import Vehicle
from missile import Missile
from gameengine import gameengine

def initparse():
    parser = ArgumentParser(description=
            "The most awesomest game written by humans!")
    return parser

def main():
    parser = initparse()
    args = parser.parse_args()

    logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

    gameengine.initialize(60000)
    gameengine.add_entity(Vehicle((50, 200), 90))
    gameengine.add_entity(Vehicle((250, 200), 90))
    gameengine.add_entity(Missile((10, 10), 1, 45, (32, 32), None))
    gameengine.start()

main()

# vim: ts=4 et tw=79 cc=+1
