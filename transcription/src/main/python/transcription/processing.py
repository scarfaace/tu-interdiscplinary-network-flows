import csv

from transcription.flows.KeyGenerator import TcpPacketEntryKeyGenerator
from transcription.StreamFlusher import StreamFlusher
from transcription.symbol_generator import CommunicationGapsGenerator, TcpLenSymbolGenerator


class TcpPacket:
    def __init__(self, timestamp, ip_protocol, ip_source, ip_dest, tcp_len):
        self.timestamp = timestamp
        self.ip_protocol = ip_protocol
        self.ip_source = ip_source
        self.ip_dest = ip_dest
        self.tcp_len = tcp_len

    @classmethod
    def build_from_row(cls, row):
        return TcpPacket(
            timestamp=float(row[0]),
            ip_protocol=int(row[1]),
            ip_source=row[2],
            ip_dest=row[3],
            tcp_len=int(row[4])
        )







class InputFileProcessor:

    def __init__(self):
        self.streams = {}
        self.streams_last_timestamps = {}
        self.min_time = None


    def process(self, input_file_name):
        with open(input_file_name, newline='') as csvfile:
            iterator = 0
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)        # skip header
            for row in csv_reader:
                if not self.__is_row_tcp_packet(row):
                    continue
                entry = TcpPacket.build_from_row(row)
                if self.min_time is None:
                    self.min_time = entry.timestamp

                key = TcpPacketEntryKeyGenerator.generate_key(self.streams, entry)
                if key not in self.streams.keys():
                    self.streams[key] = []
                    self.streams_last_timestamps[key] = entry.timestamp

                self.__generate_output_symbols(entry, key)

                self.streams_last_timestamps[key] = float(entry.timestamp)

                iterator += 1
                if iterator == 100000:
                    iterator = 0
                    self.__flush()

            self.__flush()
        return self.streams


    def __flush(self):
        StreamFlusher.flush(self.streams)
        for key in self.streams:
            self.streams[key].clear()


    def __is_row_tcp_packet(self, row):
        return int(row[1]) == 6


    def __generate_output_symbols(self, entry, key):
        comm_gaps = CommunicationGapsGenerator.generate(entry, self.streams_last_timestamps[key])
        symbol = TcpLenSymbolGenerator.generate(entry)
        self.streams[key].extend(comm_gaps)
        self.streams[key].append(symbol)



class CommunicationDirectionDecider:
    @classmethod
    def decide_communication_direction(cls, key, entry) -> int:
        ip_left, ip_right = cls.__split_key_to_ip_addresses(key)
        if entry.ip_source == ip_left:
            return 65
        if entry.ip_source == ip_right:
            return 97

    @classmethod
    def __split_key_to_ip_addresses(cls, key) -> tuple:
        split = key.split('-')
        ip_left = split[0]
        ip_right = split[1]
        return ip_left, ip_right

