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

        def load_sliced_sprites(self, w, h, filename):
	    images = []

            master_image = pygame.image.load(filename).convert()
	    #colorkey = (1,255,243)
	    colorkey = master_image.get_at((0,0))
            master_image.set_colorkey(colorkey, pygame.RLEACCEL)

	    master_width, master_height = master_image.get_size()
        
            for i in xrange(int(master_width/w)):
	        images.append(master_image.subsurface((i*w,0,w,h)))
	    return images

	def draw(self, screen):
		raise NotImplementedError("Not implemented")

def main():
	"""Unit test procedure"""
	foo = Foo()

if __name__ == "__main__":
	main()
