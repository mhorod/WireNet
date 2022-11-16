from queue import Queue

from wire import *
import sys


class Receiver:
    def __init__(self, window_size, decoder):
        self.window_size = window_size
        self.decoder = decoder
        self.packets = Queue()
        self.connection = None

    def has_packet(self):
        return not self.packets.empty()

    def get_packet(self):
        return self.packets.get()

    def run(self, connection):
        self.connection = connection
        while True:
            self.receive_bits()

    def receive_bits(self):
        signal = self.receive_signal(self.window_size)
        bit, _ = self.signal_to_bits(signal)
        if bit is not None:
            self.decoder.push_bit(bit)
            if self.decoder.has_packet():
                packet = self.decoder.get_packet()
                self.packets.put(packet)
                print("Received packet: " + str(packet))
        else:
            self.decoder.reset()

    def sync(self):
        signal = self.receive_signal(2 * self.window_size)
        best_index = 0
        best_strength = 0
        for i in range(0, self.window_size):
            bits, strength = self.signal_to_bits(
                signal[i:i + self.window_size])

            if bits is not None and strength > best_strength:
                best_index = i
                best_strength = strength

        underflow = best_index + self.window_size - len(signal)
        self.receive_signal(underflow)

    def receive_signal(self, bit_count):
        signal = []
        for _ in range(bit_count):
            self.connection.send(b'?')
            state = str(self.connection.recv(1), 'utf-8')
            print(state, end="")
            sys.stdout.flush()
            signal.append(Wire.from_string(state))
        return signal

    def signal_to_bits(self, signal):
        plus_count, minus_count = 0, 0
        for bit in signal:
            if bit == Wire.PLUS:
                plus_count += 1
            elif bit == Wire.MINUS:
                minus_count += 1
            elif bit == Wire.INVALID:
                return None, None

        if plus_count > minus_count:
            return 1, plus_count / len(signal)
        elif minus_count > plus_count:
            return 0, minus_count / len(signal)
        else:
            return None, None
