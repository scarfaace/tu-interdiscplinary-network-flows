import csv
from math import floor

from python.transcription.arguments import MyArgumentsParser


class StreamEntry:
    @staticmethod
    def build_from_row(row):
        return StreamEntry(
            timestamp=float(row[0]),
            ip_protocol=int(row[1]),
            ip_source=row[2],
            ip_dest=row[3],
            tcp_flags=row[4],
            tcp_len=int(row[5])
        )

    def __init__(self, timestamp, ip_protocol, ip_source, ip_dest, tcp_flags, tcp_len):
        self.timestamp = timestamp
        self.ip_protocol = ip_protocol
        self.ip_source = ip_source
        self.ip_dest = ip_dest
        self.tcp_flags = tcp_flags
        self.tcp_len = tcp_len


def generate_communication_gaps(entry, stream_last_time):
    time_diff = entry.timestamp - stream_last_time
    time_diff_tens_ms = floor(time_diff/0.1)
    gaps = []
    for tens_ms_inc in range(time_diff_tens_ms):
        gaps.append("-")
    return gaps


def generate_output_symbol(entry):
    symbol = int(entry.tcp_len / 146)
    return symbol




if __name__ == '__main__':

    my_arguments_parser = MyArgumentsParser()
    arguments = my_arguments_parser.parse_arguments()

    streams = {}
    streams_last_timestamps = {}
    min_time = None

    with open(arguments.filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            entry = StreamEntry.build_from_row(row)
            # print(', '.join(row))
            if entry.ip_protocol != 6:
                continue
            hosts_pair_key = None
            hosts_pair = entry.ip_source + "-" + entry.ip_dest
            hosts_pair_inverse = entry.ip_dest + "-" + entry.ip_source

            if min_time is None:
                min_time = entry.timestamp

            current_time = floor(float(entry.timestamp)) - min_time

            if hosts_pair not in streams.keys() and hosts_pair_inverse not in streams.keys():
                hosts_pair_key = hosts_pair
                streams[hosts_pair_key] = []
                streams_last_timestamps[hosts_pair_key] = entry.timestamp

            if hosts_pair in streams.keys():
                hosts_pair_key = hosts_pair
            if hosts_pair in streams.keys():
                hosts_pair_key = hosts_pair_inverse

            comm_gaps = generate_communication_gaps(entry, streams_last_timestamps[hosts_pair_key])
            symbol = generate_output_symbol(entry)

            streams[hosts_pair_key].append(comm_gaps)
            streams[hosts_pair_key].append(symbol)
