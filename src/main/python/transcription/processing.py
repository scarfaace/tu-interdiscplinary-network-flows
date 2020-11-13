import csv
from math import floor

from python.transcription.symbol_generator import CommunicationGapsGenerator, TcpLenSymbolGenerator


class StreamEntry:
    def __init__(self, timestamp, ip_protocol, ip_source, ip_dest, tcp_flags, tcp_len):
        self.timestamp = timestamp
        self.ip_protocol = ip_protocol
        self.ip_source = ip_source
        self.ip_dest = ip_dest
        self.tcp_flags = tcp_flags
        self.tcp_len = tcp_len

    @classmethod
    def build_from_row(cls, row):
        return StreamEntry(
            timestamp=float(row[0]),
            ip_protocol=int(row[1]),
            ip_source=row[2],
            ip_dest=row[3],
            tcp_flags=row[4],
            tcp_len=int(row[5])
        )


class KeysGenerator:
    @classmethod
    def generate_key(cls, streams, entry):
        hosts_pair, hosts_pair_inverse = cls.generate_possible_keys(entry)
        if hosts_pair not in streams.keys() and hosts_pair_inverse not in streams.keys():
            return hosts_pair
        if hosts_pair in streams.keys():
            return hosts_pair
        if hosts_pair_inverse in streams.keys():
            return hosts_pair_inverse

    @classmethod
    def generate_possible_keys(cls, entry):
        hosts_pair = entry.ip_source + "-" + entry.ip_dest
        hosts_pair_inverse = entry.ip_dest + "-" + entry.ip_source
        return hosts_pair, hosts_pair_inverse




class InputFileProcessor:

    def __init__(self):
        self.streams = {}
        self.streams_last_timestamps = {}
        self.min_time = None


    def process(self, input_file_name):
        with open(input_file_name, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                entry = StreamEntry.build_from_row(row)
                # print(', '.join(row))
                if entry.ip_protocol != 6:
                    continue
                if min_time is None:
                    min_time = entry.timestamp


                key = KeysGenerator.generate_key(self.streams, entry)
                if key not in self.streams.keys():
                    self.streams[key] = []
                    self.streams_last_timestamps[key] = entry.timestamp

                self.generate_output_symbols(entry, key)

                self.streams_last_timestamps[key] = floor(float(entry.timestamp))

    def generate_output_symbols(self, entry, key):
        comm_gaps = CommunicationGapsGenerator.generate(entry, self.streams_last_timestamps[key])
        symbol = TcpLenSymbolGenerator.generate(entry)
        self.streams[key].append(comm_gaps)
        self.streams[key].append(symbol)
