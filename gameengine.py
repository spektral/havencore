#!/usr/bin/python2
# encoding: utf-8
# Author: Christofer Odén

import pygame
from pygame.locals import *
import entity

class GameEngine:
    def __init__(self, screen_res):
        print "Initializing pygame..."
        pygame.init()
        self.screen = pygame.display.set_mode(screen_res)
        pygame.display.set_caption("pybattle")

        self.entities = []

    def start(self):
        self.is_running = True
        while(self.is_running):
            self.handle_input()
            self.update()
            self.draw()

    def quit(self):
        self.is_running = False

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

    def update(self):
        for entity in self.entities:
            entity.update()

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
