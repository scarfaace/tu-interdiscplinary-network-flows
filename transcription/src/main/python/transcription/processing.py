import csv

from transcription.flows.KeyGenerator import TcpPacketEntryKeyGenerator
from transcription.StreamFlusher import StreamFlusher
from transcription.symbol_generator import CommunicationGapsGenerator, TcpLenSymbolGenerator


class Packet:
    def __init__(self, timestamp, protocol_identifier, ip_source, ip_dest, tcp_len):
        self.timestamp = timestamp
        self.protocol_identifier = protocol_identifier
        self.ip_source = ip_source
        self.ip_dest = ip_dest
        self.tcp_len = tcp_len

    @classmethod
    def build_from_row(cls, row):
        return Packet(
            timestamp=float(row[0]),
            protocol_identifier=int(row[1]),
            ip_source=row[2],
            ip_dest=row[3],
            tcp_len=int(row[4])
        )







class InputFileProcessor:

    def __init__(self):
        self.ACTIVE_TIMEOUT_SECONDS = 60

        self.streams = {}
        self.streams_first_timestamps = {}
        self.streams_last_timestamps = {}
        self.min_time = None
        self.communication_gaps_generator = CommunicationGapsGenerator()


    def process(self, input_file_name):
        with open(input_file_name, newline='') as csvfile:
            iterator = 0
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)        # skip header
            for row in csv_reader:
                entry = Packet.build_from_row(row)
                if not self.__is_tcp_packet(entry):
                    continue
                if self.min_time is None:
                    self.min_time = entry.timestamp

                key = TcpPacketEntryKeyGenerator.generate_key(self.streams, entry)
                if key not in self.streams.keys():
                    self.streams[key] = []
                    self.streams_first_timestamps[key] = float(entry.timestamp)
                    self.streams_last_timestamps[key] = float(entry.timestamp)

                if self.__is_flow_timed_out(key):
                    continue

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


    def __is_tcp_packet(self, packet: Packet):
        return packet.protocol_identifier == 6


    def __generate_output_symbols(self, entry, key):
        communication_gaps: list = self.communication_gaps_generator.generate(entry, self.streams_last_timestamps[key])
        symbol = TcpLenSymbolGenerator.generate(entry, key)
        self.streams[key].extend(communication_gaps)
        self.streams[key].append(symbol)

    def __is_flow_timed_out(self, key: str):
        first_and_last_timestamp_diff_ms = self.streams_last_timestamps[key] - self.streams_first_timestamps[key]
        first_and_last_timestamp_diff_seconds = first_and_last_timestamp_diff_ms / 1000
        if first_and_last_timestamp_diff_seconds >= self.ACTIVE_TIMEOUT_SECONDS:
            return True
        return False


