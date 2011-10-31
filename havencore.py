#!/usr/bin/python2
# -*- coding: utf8 -*-

"""
Script for launching the game in different modes.

"""

import logging
import argparse
import os
import time
from server.gameengine import gameengine as serverengine
from client.gameengine import gameengine as clientengine

__author__    = "Christofer Odén"
__copyright__ = "Copyright 2011 Daladevelop"
__license__   = "GPL"

def start_singleplayer(name, addr):
    if os.fork():
        serverengine.initialize(addr[1])
        serverengine.start()
    else:
        time.sleep(0.2)
        clientengine.initialize(name, addr)
        clientengine.start()

def setup_logging(debug):
    if debug:
        output = logging.DEBUG
    else:
        output = logging.INFO

    logging.basicConfig(filename='havencore.log', filemode='w', level=output)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    console.setFormatter(formatter)
    console.setLevel(output)
    logging.getLogger().addHandler(console)

def parse_args():
    parser = argparse.ArgumentParser(
            description='Haven Core, the most awesomest game ever to be '
                        'written by humans!')

    mode = parser.add_mutually_exclusive_group()
    output = parser.add_mutually_exclusive_group()

    mode.add_argument('host', nargs='?', default='127.0.0.1',
            help='server hostname or IP address to connect to')
    mode.add_argument('-s', '--single-player', action='store_true',
            help='start a local server and connect to it as a client')
    parser.add_argument('-l', '--listen', action='store_true',
            help='start as server')
    parser.add_argument('-p', '--port', type=int, default=60000,
            help='the port to listen on or connect to')
    parser.add_argument('-n', '--name', default="Player",
            help='sets your player name')
    output.add_argument('-v', '--verbose', action='store_true',
            help='show debug output')
    parser.add_argument

    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args.verbose)

    if args.single_player:
        logging.info("Running in single player mode...")
        start_singleplayer(args.name, (args.host, args.port))
        return

    gameengine = None
    if args.listen:
        logging.info("Running in server mode...")
        serverengine.initialize(args.port)
        gameengine = serverengine
    else:
        logging.info("Running in client mode...")
        clientengine.initialize(args.name, (args.host, args.port))
        gameengine = clientengine
    gameengine.start()


main()

# vim: ts=4 et tw=79 cc=+1
