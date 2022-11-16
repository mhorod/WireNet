#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import argparse
import datetime
import logging
import os
import pathlib
import socket
import threading
import time

LOCATION = '/tmp/shared_state.sock'
DELAY = 0.25
READS = 2


class State:

    def __init__(self, delay):
        self.delay = delay
        self.state = 0
        self.last_modified = datetime.datetime.now()

    def read(self):
        now = datetime.datetime.now()
        if self.last_modified + self.delay < now:
            self.state = 0
        if self.state == 0:
            return '0'
        if self.state > 0:
            return '+'
        if self.state < 0:
            return '-'
        return '#'

    def write(self, value):
        now = datetime.datetime.now()
        if self.last_modified + self.delay < now:
            self.state = 0
        self.last_modified = now
        if self.state != 0:
            self.state = float('nan')
        elif value == '+':
            self.state = 1
        elif value == '-':
            self.state = -1
        else:
            self.state = float('nan')


parser = argparse.ArgumentParser(description='Shared State Server')
parser.add_argument('--location', default=LOCATION)
parser.add_argument('--delay', type=float, default=DELAY)
parser.add_argument('--reads', type=int, default=READS)
args = parser.parse_args()

state = State(datetime.timedelta(seconds=args.delay))
read_delay = state.delay/args.reads

if os.path.exists(args.location):
    try:
        os.remove(args.location)
    except OSError:
        pass
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server_socket:
    try:
        server_socket.bind(args.location)
        server_socket.listen(10)
        while True:
            (client_socket, client_address) = server_socket.accept()
            logging.info(f'Client {client_address} connected')

            def client_thread(client_socket):
                try:
                    while True:
                        command = client_socket.recv(1)
                        if not command:
                            return
                        if command == b'?':
                            time.sleep(read_delay.total_seconds())
                            try:
                                client_socket.send(bytes(state.read(), 'utf8'))
                            except OSError:
                                return
                        elif command in [b'+', b'-']:
                            state.write(str(command, 'utf8'))
                finally:
                    client_socket.close()
            threading.Thread(target=client_thread,
                             args=(client_socket,)).start()
    finally:
        server_socket.close()
        try:
            os.remove(args.location)
        except OSError:
            pass
