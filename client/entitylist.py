#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""Provides containers for entities"""

import logging

__author__    = "Christofer Odén"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"


# We don't need any more layers at the moment
BACKGROUND = 0
SERVER = 1
LOCAL = 2


#class GrowingList(list):
#
#    """Subclass of list, automatically expands itself"""
#
#    def __setitem__(self, index, value):
#    
#        """Expand to fit the new index if too small.  Fill the expanded
#        area with empty lists to work flawlessly with EntityContainer."""
#
#        if index >= len(self):
#            self.extend([[]] * (index + 1 - len(self)))
#
#        list.__setitem__(self, index, value)


class EntityContainer:
    
    """Provide a container for entities.
    
    Entities are grouped by layer.  Entities belonging to lower layers
    will be updated and drawn before entities in higher layers.  An
    example use of layers is to put background tiles behind player
    vehicles."""

    def __init__(self):
        self.logger = logging.getLogger('client.entitylist.EntityContainer')
        self.layers = [[]] * 3
        self.logger.debug("self.layers: %s" % (self.layers,))

    def append(self, layer, entity):

        """Add an entity to the container"""

        self.logger.debug("layer: %s, entity: %s" % (layer, entity))
        self.layers[layer].append(entity)

    def clean_dead(self):

        """Remove entities that aren't alive"""

        for layer in self.layers:
            for n in range(len(layer) - 1, -1, -1):
                if not layer[n].alive:
                    del layer[n]

    def handle_event(self, event):

        """Triggers the event handler for all entities"""

        for layer in self.layers:
            for entity in layer:
                entity.handle_input(event)

    def update(self):

        """Triggers the update handler for all entities"""

        for layer in self.layers:
            for entity in layer:
                entity.update()

    def draw(self):

        """Triggers the draw handler for all entities"""

        for layer in self.layers:
            for entity in layer:
                entity.draw()

    def get_with_serial(self, serial, layer=None):

        """Search for an entity with matching serial, return result."""

        #self.logger.debug("Serial<%s> Layer<%s>" % (serial, layer))
#        layers = []
#
#        if layer:
#            layers = [layer]
#
#        else:
#            layers = self.layers
#
#        for layer in self.layers:
        #self.logger.debug("Layers: %s" % repr(self.layers))
        for entity in self.layers[SERVER]:
            try:
                if entity.serial == serial:
                    return entity
            except AttributeError:
                pass

        return None


entity_container = EntityContainer()
