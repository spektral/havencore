#!/usr/bin/python2
#coding=UTF-8
#========================================================================
# File: jukebox.py
#
# Author: Emil Österlund ->> larsemil.se
# Date: 2011-10-22
# Licens: GPL
#
# Comment:
#
#========================================================================

import glob
import pygame
from pygame.locals import * 

class JukeBox:
	def __init__(self):
		self.soundPath = 'sounds/'
		self.musicPath = 'music/'

		self.songs = glob.glob(self.musicPath+'*.ogg')
		self.sounds = {}
		counter = 0
		for track in self.songs:
			self.songs[counter] = track
			counter = counter +1
		self.track = 0
		self.play_song(self.track)

	def play_song(self, track = 0):
		print "Playing song: "+ str(track) +". "+ self.songs[track]
		pygame.mixer.music.load(self.songs[track])
		pygame.mixer.music.play()

	def update(self):
		if self.track +1 < len(self.songs): 
			self.track = self.track +1
		else:
			self.track = 0

		if pygame.mixer.music.get_busy():
			return
		else:
			self.playSong(self.track)

	def load_sound(self, path, name):
		self.sounds[name] = pygame.mixer.Sound(self.soundPath+path)
	
	def play_sound(self, name):
		self.sounds[name].play()

