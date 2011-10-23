#!/usr/bin/python2
#coding=UTF-8
#--------------------------------------
#Name: vehicle.py
#Class for the vehicles, handles 
#input, update, draw...
#
#Gustav Fahlén, 2011-10-22
#-------------------------------------
import pygame
from pygame.locals import *
import entity
import math
from math import floor

class Vehicle(entity.Entity):
	def __init__(self, x_pos, y_pos, rotation):
		self.x_pos=x_pos
		self.y_pos=y_pos
		self.rotation=rotation
		self.rotation_torque=0
		self.velocity=0
		#self.car = pygame.image.load("car.png")
		#self.car.convert_alpha(self.car)
		#colorkey = self.car.get_at((0,0))
		#self.car.set_colorkey(colorkey, RLEACCEL)
		self.cars = self.load_sliced_sprites(40, 40, 'car2.png')
		self.carIndex = 0

	def load_sliced_sprites(self, w, h, filename):
		images = []

		master_image = pygame.image.load(filename)
		master_image.convert_alpha()
		colorkey = master_image.get_at((1,1))
		master_image.set_colorkey(colorkey, RLEACCEL)

		master_width, master_height = master_image.get_size()

		for i in xrange(int(master_width/w)):
			images.append(master_image.subsurface((i*w,0,w,h)))
		return images

	def handle_input(self, event):
		if event.type == KEYDOWN:
			if event.key == K_UP:
				self.velocity -= 5
			if event.key == K_DOWN:
				self.velocity += 5
			if event.key == K_RIGHT:
				self.rotation_torque -= 0.1
			if event.key == K_LEFT:
				self.rotation_torque += 0.1
		elif event.type == KEYUP:
			if event.key == K_UP:
				self.velocity += 5
			if event.key == K_DOWN:
				self.velocity -= 5
			if event.key == K_RIGHT:
				self.rotation_torque += 0.1
			if event.key == K_LEFT:
				self.rotation_torque -= 0.1
	
	def spriteIndex(self,v):
		C = (8/360)
	 	return int(floor((C*(v+22.5)))) % 8

	def update(self):
		self.rotation += self.rotation_torque
		while self.rotation <= 360:
			self.rotation += 360
		while self.rotation >= 360:
			self.rotation -= 360
		self.x_pos+=(self.velocity * math.sin(self.rotation))
		self.y_pos+=(self.velocity * math.cos(self.rotation))
		self.carIndex = self.spriteIndex(self.rotation)

	def draw(self, screen):
		#pygame.draw.circle(screen, pygame.Color(255,255,255), (int(self.x_pos), int(self.y_pos)), 25)
		screen.blit(self.cars[self.carIndex], (int(self.x_pos - 20), int(self.y_pos - 20)))
	
	def __repr__(self):
		return "rot: %.2f, pos: (%.2f, %.2f)" % (self.rotation, self.x_pos, self.y_pos)

# debug main
if __name__ == "__main__":
	print "test_main"
	V = Vehicle(4.0,11.0,90)
	print V

