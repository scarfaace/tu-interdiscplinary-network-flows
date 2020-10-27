import csv
from math import floor

from python.transcription.keys import KeysGenerator
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



class InputFileProcessor:

    @classmethod
    def process(cls, input_file_name):
        streams = {}
        streams_last_timestamps = {}
        min_time = None

        with open(input_file_name, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                entry = StreamEntry.build_from_row(row)
                # print(', '.join(row))
                if entry.ip_protocol != 6:
                    continue
                if min_time is None:
                    min_time = entry.timestamp


                key = KeysGenerator.generate_key(streams, entry)
                if key not in streams.keys():
                    streams[key] = []
                    streams_last_timestamps[key] = entry.timestamp

                comm_gaps = CommunicationGapsGenerator.generate(entry, streams_last_timestamps[key])
                symbol = TcpLenSymbolGenerator.generate(entry)

                streams_last_timestamps[key] = floor(float(entry.timestamp))

                streams[key].append(comm_gaps)
                streams[key].append(symbol)