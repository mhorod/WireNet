from socket import *
from queue import Queue

from wire import *

LOCATION = '/tmp/shared_state.sock'
HOST = '20.123.10.179'
PORT = 3333

DELAY = 0.25


class Receiver:
    def __init__(self, window_size, decoder):
        self.window_size = window_size
        self.decoder = decoder
        self.frames = Queue()
        self.connection = None

    def has_frame(self):
        return not self.frames.empty()

    def get_frame(self):
        return self.frames.get()
    
    def run(self, connection):
        self.connection = connection
        self.sync()
        while True:
            self.receive_signal()

    def receive_signal(self):
        bits = self.receive_bits(self.window_size)
        signal, _ = self.bits_to_signal(bits)
        if signal is not None:
            self.decoder.add_signal(signal)
            if self.decoder.has_frame():
                self.frames.put(self.decoder.get_frame())
        else:
            self.decoder.reset()

    def sync(self):
        bits = self.receive_bits(2 * self.window_size)
        best_index = 0
        best_strength = 0
        for i in range(0, self.window_size):
            signal, strength = self.bits_to_signal(bits[i:i + self.window_size])

            if signal is not None and strength > best_strength:
                best_index = i
                best_strength = strength

        underflow = best_index + self.window_size - len(bits)
        self.receive_bits(underflow)


    def receive_bits(self, bit_count):
        bits = []
        for _ in range(bit_count):
            while True:
                self.connection.send(b'?')
                state = str(self.connection.recv(1), 'utf-8')
                bits.append(Wire.from_string(state))
        return bits


    def bits_to_signal(self, bits):
        plus_count, minus_count = 0, 0
        for bit in bits:
            if bit == Wire.PLUS:
                plus_count += 1
            elif bit == Wire.MINUS:
                minus_count += 1
            elif bit == Wire.INVALID:
                return None, None

        if plus_count > minus_count:
            return 1, plus_count / len(bits)
        elif minus_count > plus_count:
            return 0, minus_count / len(bits)
        else:
            return None, None


def connect_to_remote(host, port):
    with socket(AF_INET, SOCK_STREAM) as connection:
        connection.connect((host, port))
        return connection

def connect_to_local(location):
    with socket(AF_UNIX, SOCK_STREAM) as connection:
        connection.connect(location)
        return connection 