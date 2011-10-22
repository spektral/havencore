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
import entity

class Vehicle(entity.Entity):
	#def __init__(self):
	#	self.x_pos=0.0
	#	self.ypos=0.0
	#	self.rotation=0
	#	self.rotation_torque=0

	def __init__(self, x_pos, y_pos, rotation):
		self.x_pos=x_pos
		self.y_pos=y_pos
		self.rotation=rotation
		self.rotation_torque=0
	
	def handle_input(self, event):
		pass #so far, does nothing
	
	def update(self):
		pass #so far, does nothing
	
	def draw(self, screen):
		pygame.draw.rect(screen, pygame.Color(255,0,0), (10,10,50,100))

	def __repr__(self):
		return "rot: %.2f, pos: %.2f" % (self.x_pos, self.rotation)

# debug main
if __name__ == "__main__":
	print "test_main"
	V = Vehicle(0.0,0.0,90)
	print V

