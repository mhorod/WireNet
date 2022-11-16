from sender import *
from receiver import *
from packet import *
from packet_encoding import *
from connect import *

from threading import Thread


def start_receiver():
    with connect_to_local("/tmp/shared_state.sock") as connection:
        receiver = Receiver(2, Decoder())
        print("receiving data")
        receiver.run(connection)


Thread(target=start_receiver).start()
