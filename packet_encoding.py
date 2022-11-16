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

    def set_previous_stage_result(self, result):
        pass


class PreambleDecoder(DecoderPipelineStage):
    def __init__(self):
        self.reset()

    def reset(self):
        self.previous = None
        self.received = False

    def push_bit(self, bit):
        if bit and self.previous:
            self.received = True
        self.previous = bit

    def has(self) -> bool:
        return self.received

    def get(self):
        return None


class NumberDecoder(DecoderPipelineStage):
    def __init__(self, length):
        self.length = length
        self.reset()

    def reset(self):
        self.bits = []

    def push_bit(self, bit):
        self.bits.append(bit)

    def has(self):
        return len(self.bits) >= self.length

    def get(self):
        bytes = bits_to_bytes(self.bits[:self.length])
        return int.from_bytes(bytes, 'big')


class BytesDecoder(DecoderPipelineStage):
    def __init__(self, length):
        self.length = length
        self.reset()

    def reset(self):
        self.bits = []

    def push_bit(self, bit):
        self.bits.append(bit)

    def has(self):
        return len(self.bits) >= self.length

    def get(self):
        return bits_to_bytes(self.bits[:self.length])

    def set_previous_stage_result(self, result):
        self.length = result * 8


class DecoderPipeline:
    def __init__(self, stages):
        self.stages = stages
        self.reset()

    def reset(self):
        for stage in self.stages:
            stage.reset()
        self.current_stage = 0
        self.result = []

    def push_bit(self, bit):
        self.stages[self.current_stage].push_bit(bit)
        if self.stages[self.current_stage].has():
            print(f"Stage {self.current_stage} done")
            self.result.append(self.stages[self.current_stage].get())
            self.current_stage += 1
            if self.current_stage == len(self.stages):
                print(self.result)
                self.current_stage = 0
            else:
                self.stages[self.current_stage].set_previous_stage_result(
                    self.result[-1])

    def has(self):
        return len(self.result) == len(self.stages)

    def get(self):
        return self.result


class Decoder:
    def __init__(self):
        self.pipeline = DecoderPipeline([
            PreambleDecoder(),
            NumberDecoder(ADDRESS_LENGTH * 8),
            NumberDecoder(ADDRESS_LENGTH * 8),
            NumberDecoder(LENGTH_LENGTH * 8),
            BytesDecoder(0),
        ])
        self.reset()

    def push_bit(self, bit):
        self.pipeline.push_bit(bit)

    def push_bits(self, bits):
        for bit in bits:
            self.push_bit(bit)

    def has_packet(self):
        return self.pipeline.has()

    def get_packet(self):
        _, dest, src, _, message = self.pipeline.get()
        self.pipeline.reset()
        return Packet(dest, src, message)

    def reset(self):
        self.bits = []
        self.packet = None
        self.received_preamble = False
        self.pipeline.reset()


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
