#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Launches and initializes the game.

"""

__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

from gameengine import gameengine
from vehicle import Vehicle
from missile import Missile

gameengine.add_entity(Vehicle(200, 200, 90))
gameengine.add_entity(Missile(10, 10, 1, 45, "img/missile2.png", (32, 32), None))
gameengine.start()
