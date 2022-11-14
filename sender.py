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
        while not is_sent:
            for bit in bits:
                message = b'+' if bit == 1 else b'-'
                connection.send(message)
                state = connection.recv(1)
                if state != message:
                    self.failed_attempts += 1
                    self.backoff()
                    break
            else:
                is_sent = True
                self.failed_attempts = 0
               

    def backoff(self):
        upper_bound = self.packet_wait_time * 2 ** self.failed_attempts
        time.sleep(random.uniform(0, upper_bound))
