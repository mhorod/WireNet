import time
import random


class Sender:
    def __init__(self, encoder, packet_wait_time):
        self.encoder = encoder
        self.packet_wait_time = packet_wait_time
        self.failed_attempts = 0

    def send_packet(self, packet, connection):
        bits = self.encoder.packet_to_bits(packet)
        is_sent = False
        failed = False
        while not is_sent or failed:
            for bit in bits:
                message = b'+' if bit == 1 else b'-'
                result = self.send_message(message, connection)
                if not result:
                    failed = True
                    break

            is_sent = True

    def send_message(self, message, connection):
        connection.send(message)
        while True:
            connection.send(b'?')
            state = connection.recv(1)
            if state == b'0':
                return True
            elif state == b'#':
                self.failed_attempts += 1
                self.backoff()
                return False


    def backoff(self):
        upper_bound = self.packet_wait_time * 2 ** self.failed_attempts
        t = random.uniform(0, upper_bound)
        print(f"Collision, going to sleep for {t} seconds")
        time.sleep(t)
