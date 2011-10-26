#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
This class links the user interface to the game objects and drives the
game loop.

"""

__author__    = "Christofer Odén"
__email__     = "bei.oden@gmail.com"
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"

import pygame
from pygame.locals import *
import entity
import missile
import vehicle
import explode

class GameEngine:
    """
    Game engine is implemented according to the "Borg" pattern.  All instances
    share the same data.
    
    """
    _we_are_borg = {}

    def __init__(self, screen_res):
        self.__dict__ = self._we_are_borg

        if self.__dict__ == {}:
            print "Initializing pygame..."
            pygame.init()

            self.screen = pygame.display.set_mode(screen_res)
            pygame.display.set_caption("pybattle")

            self.fps_clock = pygame.time.Clock()

            self.entities = []
            self.entities.append(vehicle.Vehicle(200, 200, 90))
            self.entities.append(missile.Missile(10, 10, 1, 45))

    def start(self):
        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            self.collide_detect()
            self.draw()
            self.fps_clock.tick(50)

    def quit(self):
        self.is_running = False
    
    # Better name "handle_events"
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                    break

            for entity in self.entities:
                entity.handle_input(event)

        for entity in self.entities:
            entity.check_collisions(self.entities)

    def update(self):
        for entity in self.entities:
#            if entity.__class__.__name__ == "Explode":
#                if entity.unitIndex > entity.num_rec-2:
#                    self.entities.remove(entity)
            entity.update()
    
    def collide_detect(self):
        for entity in self.entities:
            if entity.collide_detect(self.entities):
                if entity.__class__.__name__ == "Missile":
                    print "Missile Collide"
                    self.entities.append(explode.Explode(entity.x_pos, entity.y_pos, 'img/explosion2.png', 18, 64))
                    self.entities.remove(entity)
                elif entity.__class__.__name__ == "Vehicle":
                    print "Vehicle Collide"


    def draw(self):
        self.screen.fill(pygame.Color(66, 66, 111))

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.display.update()


    def __repr__(self):
        return self.entities

if __name__ == "__main__":
    game_engine = GameEngine((640, 480))
    game_engine.start()
