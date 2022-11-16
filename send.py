from sender import *
from connect import *
from packet import *
from packet_encoding import *

connection = connect_to_local("/tmp/shared_state.sock")
sender = Sender(Encoder(), 0.1)
print("sending packet")
sender.send_packet(Packet(5, 6, b"abcdefghij1234"), connection)
print("sent")
