from abc import ABC, abstractmethod

from packet import *


class Encoder:
    def packet_to_bits(self, packet):
        return bytes_to_bits(encode_packet(packet))

class DecoderPipelineStage(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def push_bit(self, bit):
        pass

    @abstractmethod
    def has(self) -> bool:
        pass

    @abstractmethod
    def get(self):
        pass


class NumberDecoder(DecoderPipelineStage):
    def __init__(self, length):
        self.length = length
        self.bits = []

    def push_bit(self, bit):
        self.bits.append(bit)

    def has(self):
        return len(self.bits) >= self.length

    def get(self):
        bytes = bits_to_bytes(self.bits[:self.length])
        return int.from_bytes(bytes, 'big')

class DecoderPipeline:
    def __init__(self, stages):
        self.stages = stages
        self.current_stage = 0
        self.result = []

    def reset(self):
        for stage in self.stages:
            stage.reset()

    def push_bit(self, bit):
        self.stages[self.current_stage].push_bit(bit)
        if self.stages[self.current_stage].has():
            self.result.append(self.stages[self.current_stage].get())
            self.current_stage += 1
            if self.current_stage == len(self.stages):
                self.current_stage = 0

    def has(self):
        return len(self.result) > 0

    def get(self):
        return self.result


class Decoder:
    def __init__(self):
        self.reset()


    def push_bit(self, bit):
        self.bits.append(bit)
        if not self.received_preamble:
            if self.bits[-2:] == [1, 1]:
                self.received_preamble = True
                self.bits = []
        else:
            pass


    def has_packet(self):
        return self.packet is not None
    
    def get_packet(self):
        packet = self.packet
        self.reset()
        return packet

    def reset(self):
        self.bits = []
        self.packet = None
        self.received_preamble = False

def bits_to_bytes(bits):
    return bytes(bits_to_byte(bits[i:i + 8]) for i in range(0, len(bits), 8))

def bits_to_byte(bits):
    return sum(bit << (7 - i) for i, bit in enumerate(bits))

def bytes_to_bits(data):
    for byte in data:
        yield from byte_to_bits(byte)

def byte_to_bits(byte):
    for i in range(8):
        yield (byte >> (7 - i)) & 1