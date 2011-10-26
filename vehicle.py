#!/usr/bin/python2 -tt
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
import missile
import rotsprite
import math
import gameengine
import explosion
from math import floor, radians

class Vehicle(entity.Entity):
    def __init__(self, x, y, rot):
        entity.Entity.__init__(self, x, y, 40)
        self.rot = rot
        self.torque = 0
        self.vel = 0
        self.sprite = rotsprite.RotSprite("img/car6_fixed.png", (80,80))
        self.health = 100

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.vel += 5.0
            if event.key == K_DOWN:
                self.vel -= 5.0
            if event.key == K_RIGHT:
                self.torque -= 5.0
            if event.key == K_LEFT:
                self.torque += 5.0
            if event.key == K_SPACE:
                print "MISSILE AWAY"
                #self.ActiveMissile.append(missile.Missile(self.x, self.y, 12, self.rot))
        elif event.type == KEYUP:
            if event.key == K_UP:
                self.vel -= 5.0
            if event.key == K_DOWN:
                self.vel += 5.0
            if event.key == K_RIGHT:
                self.torque += 5.0
            if event.key == K_LEFT:
                self.torque -= 5.0

    def update(self):
        ge = gameengine.GameEngine()

        while self.collision_list:
            if isinstance(self.collision_list.pop(0), missile.Missile):
                self.health -= 40

        if self.health <= 0:
            self.health = 0
            ge.entities.append(explosion.Explosion(self.x, self.y,
                "img/explosion2.png", (64, 64), 2))
            self.alive = False

        self.rot += self.torque

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.x += (self.vel * math.sin(radians(self.rot)))
        self.y += (self.vel * math.cos(radians(self.rot)))
        self.sprite.set_direction(self.rot)

    def collide_detect(self, lst_ent):
        pass

    def draw(self, screen):
        self.sprite.draw(screen, self.x, self.y)

    def __repr__(self):
        return ("(Vehicle, alive:%s rot:%.2f, vel:%.2f, (x%.2f, y%.2f))" %
            (self.alive, self.rot, self.vel, self.x, self.y))
#
#   Unit test procedure
#
if __name__ == "__main__":
    pass

# vim: set ts=4 sw=4 et
