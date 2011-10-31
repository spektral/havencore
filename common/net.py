#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""Module for network functions used by both client and server"""

__author__    = "Christofer Odén"
__credits__   = ["Christofer Odén"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

import logging
import json
import zlib
import errno

BUFSIZE = 65536
logger = logging.getLogger('common.net')

def send(socket, message, username='server'):

    """Tag a message with username and encode it, then send it to the
    remote host assocated with the specified socket.
    
    For the server, username specification is not required."""

    message = { 'username': username, 'message': message }

    logger.debug("Sending: %s" % message.__repr__())

    try:
        message = json.dumps(message, separators=(',',':'))
    except Exception as e:
        logger.error("%s: %s" % (e.__class__.__name__, e))
        raise
        #raise IOError(0, "json.dumps failed")

    try:
        message = zlib.compress(message)
    except Exception as e:
        logger.error("%s: %s" % (e.__class__.__name__, e))
        raise
        #raise IOError(0, "zlib.compress failed")

    bytes_sent = socket.send(message)
    if bytes_sent != len(message):
        raise IOError(0, "Could not send all data")


def receive(socket):

    """Receive all pending messages from the remote host associated
    with the specified socket.
    
    If multiple messages are received, take out the username and create
    a list of the actual messages.
    
    Return username, message(s)"""

    net_data = socket.recv(BUFSIZE)

    if not net_data:
        raise IOError(errno.ECONNRESET, "Connection lost")

    data = split_zlib(net_data)

    try:
        data = map(zlib.decompress, data)
    except Exception as e:
        logger.error("%s: %s\nData: %s" %
                     (e.__class__.__name__, e, data.__repr__()))
        return None, None
        #raise IOError(0, "zlib.decompress failed")

    try:
        messages = map(json.loads, data)
    except Exception as e:
        logger.error("%s: %s" % (e.__class__.__name__, e))
        raise IOError(0, "json.loads failed")

    logger.debug("Received: %s" % messages)

    if not 'username' in messages[0]:
        raise Exception("Message list did not contain username")

    username = messages[0]['username']
    messages = [m['message'] for m in messages]

    return username, messages


def split_zlib(string):

    """Splits a string containing multiple zlib compressed substrings"""
    
    header = 'x\x9c'

    strings = []
    index = string.find(header)
    while index >= 0:
        # Find the position of the next header
        next_index = string.find(header, index + 1)

        if next_index >= 0:
            # Take all the chars up to the next header
            strings.append(string[index : next_index])
        else:
            # No more headers in the string, take all chars that's left
            strings.append(string[index:])

        # Continue at the next header's position
        index = next_index

    return strings

# vim: ts=4 et tw=79 cc=+1
