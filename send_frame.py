from socket import *
import time
import sys

from wire import *

ADDRESS_LENGTH = 1
LENGTH_LENGTH = 2

LOCATION = '/tmp/shared_state.sock'

HOST = '20.123.10.179'
PORT = 3333


DELAY = 0.1



def send_frame(frame: EthernetFrame, connection):
    bits = bytes_to_bits(encode_frame(frame))
    for bit in bits:
        connection.send(b'+' if bit else b'-')
        while True:
            connection.send(b'?')
            state = connection.recv(1)
            if state == b'0':
                break

def send_frames(frames, connection):
    for frame in frames:
        send_frame(frame, connection)
        print("frame sent")
        time.sleep(DELAY * 4)
        

def frame_message(source, dest, message):
    MAX_LEN = 1000
    frames = []
    last_msg = ""
    for m in message:
        last_msg += m
        if len(last_msg) == MAX_LEN:
            frames.append(EthernetFrame(source, dest, last_msg.encode()))
            last_msg = ""
    if last_msg:
        frames.append(EthernetFrame(source, dest, last_msg.encode()))

    return frames


def send_message(source, dest, message):
    frames = frame_message(source, dest, message)
    with socket(AF_INET, SOCK_STREAM) as connection:
        connection.connect((HOST, PORT))
        send_frames(frames, connection)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(0)
    src, dest, msg = sys.argv[1:]
    send_message(int(src), int(dest), msg)
