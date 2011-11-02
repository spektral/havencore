#!/usr/bin/python2 -tt
# -*- coding: utf-8 -*-

"""Module for network functions used by both client and server"""

__author__    = "Christofer Odén"
__credits__   = ["Christofer Odén"]
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

import select
import logging
import json
import zlib
import errno

BUFSIZE = 65536
logger = logging.getLogger('common.net')

def readable(socket):

    """Test if the socket is readable."""

    readable, writable, in_error = select.select([socket], [], [], 0)
    return (readable != [])


def writable(socket):

    """Test if the socket is writeable."""

    readable, writable, in_error = select.select([], [socket], [], 0)
    return (writable != [])


def send(socket, message, username='server'):

    """Tag a message with username and encode it, then send it to the
    remote host assocated with the specified socket.
    
    For the server, username specification is not required."""

    message = { 'username': username, 'message': message }

    #logger.debug("Sending: %s" % message.__repr__())

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

    # Put a header indicating how long the message is
    assert(len(message) < 10 ** 5)
    message = "%05d%s" % (len(message), message)

    bytes_sent = socket.send(message)
    if bytes_sent != len(message):
        raise IOError(0, "Could not send all data")

    #logger.debug("Sent message:\n%s" % repr(message))


def receive(socket):

    """Receive all pending messages from the remote host associated
    with the specified socket.
    
    If multiple messages are received, take out the username and create
    a list of the actual messages.
    
    Return username, message(s)"""

    net_data = []

    while True:
        msglen = socket.recv(5)
        if not msglen:
            raise IOError(errno.ECONNRESET, "Connection lost")

        #logger.debug("Got msglen:\n%s" % repr(msglen))

        msglen = int(msglen)

        net_data.append(socket.recv(msglen))
        if not net_data[-1]:
            raise IOError(errno.ECONNRESET, "Connection lost")

        if not readable(socket):
            break

    #logger.debug("net_data:\n%s" % repr(net_data[-1]))

    try:
        data = map(zlib.decompress, net_data)
    except Exception as e:
        logger.error("%s: %s\nData: %s" %
                     (e.__class__.__name__, e, repr(net_data)))
        return None, None

    try:
        messages = map(json.loads, data)
    except Exception as e:
        logger.error("%s: %s" % (e.__class__.__name__, e))
        raise IOError(0, "json.loads failed")

    #logger.debug("messages: %s" % messages)

    if not 'username' in messages[0]:
        raise Exception("Message list did not contain username")

    username = messages[0]['username']
    messages = [m['message'] for m in messages]

    return username, messages


def split_zlib(string):

    """Split a string containing multiple zlib compressed substrings,
    return the list of decompressed strings"""
    
    header = 'x\x9c'

    strings = []
    index = string.find(header)
    while index >= 0:
        # Find the position of the next string
        next_index = string.find(header, index + 1)

        if next_index >= 0:
            # Store all the bytes up to the next header
            strings.append(string[index : next_index])
        else:
            # There are no more substrings in the string, store the
            # rest of it
            strings.append(string[index:])

        # Continue at the next header's position
        index = next_index

    return strings

# vim: ts=4 et tw=79 cc=+1
