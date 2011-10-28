#!/usr/bin/python2

import logging
import argparse
import os
from client.vehicle import Vehicle
from server.gameengine import gameengine as serverengine
from client.gameengine import gameengine as clientengine

def start_singleplayer():
    if os.fork():
        serverengine.initialize(60000)
        serverengine.start()
    else:
        clientengine.initialize((800, 600))
        clientengine.start()

def setup_logging():
    logging.basicConfig(filename='log.log', filemode='w', level=logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(console)

def parse_args():
    # expected function:
    # ./main.py -l -p 9999
    #    start the server on port 9999
    # ./main.py 127.0.0.1 -p 9999
    #    connect to 127.0.0.1 on port 9999
    parser = argparse.ArgumentParser(description='Start the game')
    parser.add_argument('host', nargs='?', default='127.0.0.1',
            help='server hostname or IP address to connect to')
    parser.add_argument('-l', '--listen', action='store_true',
            help='start as server')
    parser.add_argument('-s', '--single-player', action='store_true',
            help='start a local server and connect to it as a client')
    parser.add_argument('-p', '--port', type=int, default=60000,
            help='the port to listen on or connect to')
    parser.add_argument

    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()

    if args.single_player:
        logging.info("Running in single player mode...")
        start_singleplayer()
        return

    gameengine = None
    if args.listen:
        logging.info("Running in server mode...")
        gameengine = serverengine
    else:
        logging.info("Running in client mode...")
        gameengine = clientengine
    gameengine.initialize(args.port)
    clientengine.add_entity(Vehicle((400, 300), 120))
    gameengine.start()


main()

# vim: ts=4 et tw=79 cc=+1
