#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

from math import *
import logging

from random import randint

import pygame
from pygame.locals import *

from gameengine import gameengine
import sqlite3

__author__    = "Gustav Fahlén, Max Sidenstjärna, Christofer Odén"
__credits__   = ["Gustav Fahlén", "Christofer Odén", "Max Sidenstjärna"]
__copyright__ = "Copyright 2011, Daladevelop"
__license__   = "GPL"


def look_at((eye_x, eye_y), (tgt_x, tgt_y)):

    """Calculate the angle of a vector"""

    nx = tgt_x - eye_x
    ny = tgt_y - eye_y

    cx, cy = (0, 1)

    norm = sqrt(nx * nx + ny * ny)
    (nx, ny) = (nx / norm, ny / norm)

    dot = nx * cx + ny * cy

    if nx < 0:
        return degrees(acos(-dot)) + 180
    else:
        return degrees(acos(dot))


class Entity(object):

    """Abstract base class for data belonging to all kinds of of game
    objects."""

    ticker = 0

    def __init__(self, player, (x, y), r):
        self.serial = Entity.ticker
        Entity.ticker += 1
        self.age = 0
        self.player = player
        self.x = x
        self.y = y
        self.r = r
        self.collision_list = []
        self.is_collidable = True
        self.alive = True

    def update(self):
        self.age += 1

    def handle_input(self, event):
        pass

    def get_state(self):

        """Return a dictionary representation of the instance."""

        # Get the state of the object
        state = { 'type': 'entity',
                  'name': self.__class__.__name__,
                  'dict': dict(self.__dict__) }

        # Weed out unnecessary fields
        blacklist = ['children', 'parent', 'collision_list', 'logger',
                'target', 'weapon']

        for item in blacklist:
            try:
                del state['dict'][item]
            except KeyError:
                pass

        return state

    def get_colliders(self):
        return self.collision_list

    def check_collisions(self, entities):
        for entity in entities:
            if entity is not self and entity.is_collidable:
                dx = entity.x - self.x
                dy = entity.y - self.y
                rr = (entity.r + self.r) / 2
                if dx * dx + dy * dy < rr * rr:
                    self.collision_list.append(entity)


class Vehicle(Entity):

    """Generic class for all types of vehicles in the game"""

    def __init__(self, player, (x, y), rot, modules):
        self.logger = logging.getLogger('server.entities.Vehicle')

        Entity.__init__(self, player, (x, y), 60)
        self.rot = rot
        self.maxvel = 0
        self.torque = 0
        self.vel = 0
        self.strafe_vel = 0
        
        #some standard values
        self.speed = 1

        self.health = 100
       
        self.active_modules = []
        #change standard values according to what modules vehicle is built of. 
        self.set_modules(modules)
        self.children = []
        self.logger.debug("HP: %s  Speed: %s" %
                          (self.health, self.speed))

        self.init_weapons()
        self.weapon = Rocket

    def init_weapons(self):

        """Initialize member data belonging to weapons"""

        self.is_firing = False
        self.is_firing_sec = False
        self.fire_delay = 5
        self.cooldown = 0

        self.maxammo = 12
        self.ammo = self.maxammo
        self.reload_time = 100
        self.reload_cooldown = 0

        self.turret_rot = 0

    def set_modules(self, modules):
        conn = sqlite3.connect('server/havencore.db')
        c = conn.cursor()
        c.execute('select * from modules')
        for module in c:
            if module[0] in modules:
                if module[0] not in self.active_modules:
                    self.active_modules.append(module[0]) #Append the module
                
                if module[1] == 'speed': #this module changes speed
                    self.speed += module[2]
                elif module[1] == 'armor':
                    self.health += module[2]

    def handle_input(self, event):

        """Handle player input"""

        if event.type == KEYDOWN:
            if event.key == K_w:
                self.vel += self.speed

            if event.key == K_s:
                self.vel -= self.speed

            if event.key == K_d:
                self.torque -= self.speed
                #self.strafe_vel -= self.speed

            if event.key == K_a:
                self.torque += self.speed
                #self.strafe_vel += self.speed

            if event.key == K_SPACE:
                self.is_firing = True

            if event.key == K_1:
                self.weapon = Rocket
                self.logger.debug("Weapon: Rocket")

            if event.key == K_2:
                self.weapon = HomingMissile
                self.logger.debug("Weapon: Homing Missile")

            if event.key == K_3:
                self.weapon = MgBullet
                self.logger.debug("Weapon: Machinegun")

            if event.key == K_4:
                self.weapon = LandMine
                self.logger.debug("Weapon: LandMine")


        elif event.type == KEYUP:
            if event.key == K_w:
                self.vel -= self.speed

            if event.key == K_s:
                self.vel += self.speed

            if event.key == K_d:
                self.torque += self.speed
                #self.strafe_vel += self.speed

            if event.key == K_a:
                self.torque -= self.speed
                #self.strafe_vel -= self.speed

            if event.key == K_SPACE:
                self.is_firing = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_firing = True
                self.turret_rot = look_at((self.x, self.y), event.pos)
            if event.button == 2:
                self.is_firing = True
                self.turret_rot = look_at((self.x, self.y), event.pos)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_firing = False
            if event.button == 2:
                self.is_firing = False

    def update(self):
        Entity.update(self)

        while self.collision_list:
            entity = self.collision_list.pop(0)
            if not entity in self.children and isinstance(entity, Missile):
                self.health -= 5

        self.children = [c for c in self.children if c.alive]


        if self.health <= 0:
            self.alive = False
        self.rot += self.torque / 4.0

        while self.rot < 0.0:
            self.rot += 360.0
        while self.rot >= 360.0:
            self.rot -= 360.0

        self.x += (self.vel * sin(radians(self.rot))) / 2.0
        self.y += (self.vel * cos(radians(self.rot))) / 2.0
        self.x += (self.strafe_vel * sin(radians(self.rot + 90.0))) / 2.0
        self.y += (self.strafe_vel * cos(radians(self.rot + 90.0))) / 2.0

        self.weapon_update()
        
    def weapon_update(self):

        if self.cooldown > 0:
            self.cooldown -= 1

        if self.reload_cooldown > 0:
            self.reload_cooldown -= 1
            self.logger.info("Time until reload: %d" % self.reload_cooldown)
            if self.reload_cooldown == 0:
                self.ammo = self.maxammo

        if self.is_firing and self.cooldown == 0 and self.ammo > 0:
           
            self.fire()

            self.cooldown = self.fire_delay
            self.ammo -= 1
            self.logger.info("Ammo: %d" % self.ammo)
            if self.ammo == 0:
                self.reload_cooldown = self.reload_time

    def fire(self):

        missile = self.weapon(self, (self.x, self.y), self.turret_rot)
        gameengine.add_entity(missile) 
        self.children.append(missile)
    
    def __repr__(self):

        """Return a string representation of the instance."""

        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Missile(Entity):

    """Generic class for all projectiles in the game."""

    def __init__(self, parent, pos, rot, vel, size, max_age):

        Entity.__init__(self, parent.player, pos, size[0] / 2)
        self.vel = vel
        self.rot = rot
        self.parent = parent
        self.max_age = max_age

    def update(self):

        """Do logic, react to collisions, move."""

        Entity.update(self)

        if self.age > self.max_age:
            self.alive = False

        self.on_collision()

        self.x += self.vel * sin(radians(self.rot))
        self.y += self.vel * cos(radians(self.rot))

    def on_collision(self):

        for entity in self.collision_list:
            if entity is not self.parent:
                self.alive = False
                break

    def __repr__(self):

        """Return a string representation of the instance."""

        return ('<%s(alive=%s, x=%0.2f, y=%0.2f, rot=%0.2f, vel=%0.2f)>' %
                (self.__class__.__name__, self.alive, self.x, self.y,
                    self.rot, self.vel))


class Rocket(Missile):

    """A dumb rocket propelled warhead."""

    def __init__(self, parent, (x, y), rot):

        Missile.__init__(self, parent, (x, y), rot + randint(-3, 3),
                vel=15, size=(32, 32), max_age=randint(48,52))


class MgBullet(Missile):

    """A dumb kinetic projectile"""

    def __init__(self, parent, (x, y), rot):

        Missile.__init__(self, parent, (x, y),
                rot=rot+randint(-3, 3), vel=50, size=(1, 1), max_age=100)


class LandMine(Missile):
    
    """An explosive charge detonating on proximity of an enemy"""

    def __init__(self, parent, (x, y), rot):

        """Take into account the rotation of the vehicle that plants
        the landmine, and adjust the position so that it appears behind
        it."""

        Missile.__init__(self, parent, (x, y),
                rot=0, vel=0, size=(3, 3), max_age=10000)
        self.x -= (6 + parent.r) * sin(radians(parent.rot))
        self.y -= (6 + parent.r) * cos(radians(parent.rot))

    def on_collision(self):

        """Don't discriminate between enemies and friendly when
        detonating."""

        if self.collision_list:
            self.alive = False


class HomingMissile(Missile):

    """A missile that seeks out the closest target"""

    def __init__(self, parent, (x, y), rot):
        Missile.__init__(self, parent, (x, y),
                rot, vel=6, size=(32,32), max_age=500)

        # Acquire a target
        distances = []
        for entity in filter(lambda x:x.player != self.player,
                                          gameengine.entities):
            dx, dy = self.x - entity.x, self.y - entity.y
            distances.append((dx*dx + dy*dy, entity))

        if not distances:
            self.target = None
        else:
            self.target = min(distances)[1]

    def update(self):
        if self.target:
            self.rot = look_at((self.x, self.y),
                               (self.target.x, self.target.y))

        Missile.update(self)


# vim: ts=4 et tw=79 cc=+1
