#!/usr/bin/python2 -tt
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

import logging
from os import path
import glob
import pygame
from pygame.locals import * 

__author__    = "Emil Österlund"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

class JukeBox:
    def __init__(self):
        self.logger = logging.getLogger('client.jukebox.JukeBox')
        self.sounds = {}
        self.tracks = []
        self.track = 0

    def initialize(self):
        self.load_resources()
        self.play_song(self.track)

    def load_resources(self):

        """Preload all sound effect files and fill the tracks list
        with music files."""

        dir = path.dirname(__file__)
        self.sound_path = path.join(dir, 'sounds/')
        self.music_path = path.join(dir, 'music/')

        music_files = glob.glob(path.join(self.music_path, '*.ogg'))
        self.logger.debug("Loading music files: %s" % music_files)
        for filename in music_files:
            self.tracks.append(filename)

        self.sounds['rocket'] = pygame.mixer.Sound(path.join(self.sound_path,
                                                             'rocket1.ogg'))
        self.sounds['missile_boom'] = pygame.mixer.Sound(
                path.join(self.sound_path, 'missile-boom.ogg'))
        self.sounds['vehicle_boom'] = pygame.mixer.Sound(
                path.join(self.sound_path, 'vehicle-boom.ogg'))

    def play_song(self, track = 0):
        pygame.mixer.music.load(self.tracks[track])
        pygame.mixer.music.play()

    def update(self):

        if pygame.mixer.music.get_busy():
            return
        else:
            if self.track +1 < len(self.songs): 
                self.track = self.track +1
            else:
                self.track = 0
    
            self.play_song(self.track)
    
    def play_sound(self, name):
        self.logger.info("Play sound: %s" % name)
        self.sounds[name].play()

jukebox = JukeBox()

# vim: ts=4 et tw=79 cc=+1
