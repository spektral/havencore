#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""
Abstract base class for a common interface to all game objects.

"""

__author__    = "Christofer Odén"
__email__     = "bei.oden@gmail.com"
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import pygame

class Entity:
	def handle_input(self, event):
		raise NotImplementedError("Not implemented")

	def update(self):
		raise NotImplementedError("Not implemented")
	
        def collide_detect(self, lst_ent):
		raise NotImplementedError("Not implemented")

	def draw(self, screen):
		raise NotImplementedError("Not implemented")

def main():
	"""Unit test procedure"""
	foo = Foo()

if __name__ == "__main__":
	main()
