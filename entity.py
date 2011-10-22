#!/usr/bin/python2 -tt

import pygame

class Entity:
	"""
	Abstract base class.  All game objects should inherit from this.

	"""
	def handle_input(self, event):
		raise NotImplementedError("Not implemented")

	def update(self):
		raise NotImplementedError("Not implemented")

	def draw(self, screen):
		raise NotImplementedError("Not implemented")

def main():
	"""Unit test procedure"""

if __name__ == "__main__":
	main()
