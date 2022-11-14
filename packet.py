from dataclasses import dataclass

ADDRESS_LENGTH = 1
LENGTH_LENGTH = 2
CHECKSUM_LENGTH = 4

@dataclass
class Packet:
    destination: int
    source: int
    message: bytes


def encode_preamble():
    return bytes([0b10101010] * 0 + [0b10101011])

def encode_address(address):
    return address.to_bytes(ADDRESS_LENGTH, 'big')

def decode_address(data):
    return int.from_bytes(data, 'big')

def encode_message(data):
    length = len(data)
    lb = length.to_bytes(LENGTH_LENGTH, 'big')
    return lb + data

def decode_message(data):
    length = int.from_bytes(data[:LENGTH_LENGTH], 'big')
    return data[LENGTH_LENGTH:LENGTH_LENGTH + length]


def encode_packet(packet: Packet):
    packet_content = (
        encode_address(packet.destination)
        + encode_address(packet.source)
        + encode_message(packet.message)
    )
    return encode_preamble() + packet_content

def bits_to_byte(bits):
    return sum(bit << (7 - i) for i, bit in enumerate(bits))

def bytes_to_bits(data):
    for byte in data:
        yield from byte_to_bits(byte)


def byte_to_bits(byte):
    for i in range(8):
        yield (byte >> (7 - i)) & 1