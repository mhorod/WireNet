from packet_encoding import *
from packet import *


def test_decoding_encoded_packet_yields_the_same_packet():
    packet = Packet(7, 1, b"Hello")
    bits = Encoder().packet_to_bits(packet)
    decoder = Decoder()
    decoder.push_bits(bits)

    print(decoder.pipeline.get())
    print(decoder.get_packet())


test_decoding_encoded_packet_yields_the_same_packet()
