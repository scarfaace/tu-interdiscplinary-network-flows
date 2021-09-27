import csv
import sys

from transcription.StreamFlusher import StreamFlusher
from transcription.symbol_generator import CommunicationGapsGenerator, TcpLenSymbolGenerator

csv.field_size_limit(sys.maxsize)



class ExtractedFeaturesRow:
    def __init__(self, flowStartMilliseconds, flowDurationMilliseconds, sourceIPAddress, destinationIPAddress,
                 packetTotalCount, accumulate_ipTotalLength, accumulate_interPacketTimeMilliseconds, accumulate_flowDirection):
        self.flowStartMilliseconds = flowStartMilliseconds
        self.flowDurationMilliseconds = flowDurationMilliseconds
        self.sourceIPAddress = sourceIPAddress
        self.destinationIPAddress = destinationIPAddress
        self.packetTotalCount = packetTotalCount
        self.accumulate_ipTotalLength = accumulate_ipTotalLength
        self.accumulate_interPacketTimeMilliseconds = accumulate_interPacketTimeMilliseconds
        self.accumulate_flowDirection = accumulate_flowDirection

    @classmethod
    def build_from_row(cls, row):
        return ExtractedFeaturesRow(
            flowStartMilliseconds=float(row[0]),
            flowDurationMilliseconds=float(row[1]),
            sourceIPAddress=row[2],
            destinationIPAddress=row[3],
            packetTotalCount=row[4],
            accumulate_ipTotalLength=cls.parse_row_array_integers(row[5]),
            accumulate_interPacketTimeMilliseconds=cls.parse_row_array_integers(row[6]),
            accumulate_flowDirection=cls.parse_row_array_booleans(row[7])
        )

    @classmethod
    def parse_row_array_integers(cls, rowArray: str):
        if rowArray is None or rowArray == '':
            return []
        rowArrayCleaned = rowArray[1:len(rowArray)-1]
        return list(map(lambda x: int(x), rowArrayCleaned.split(' ')))

    @classmethod
    def parse_row_array_booleans(cls, rowArray: str):
        if rowArray is None or rowArray == '':
            return []
        rowArrayCleaned = rowArray[1:len(rowArray)-1]
        return list(map(lambda x: True if x == "true" else False, rowArrayCleaned.split(' ')))


class Transcription:
    def __init__(self, flowStartMilliseconds: int, flowDurationMilliseconds: int, transcriptionString: str):
        self.flowStartMilliseconds = flowStartMilliseconds
        self.flowDurationMilliseconds = flowDurationMilliseconds
        self.transcriptionString = transcriptionString




class InputFileProcessor:

    def __init__(self):
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
                # print(iterator)
                row = ExtractedFeaturesRow.build_from_row(row)

                key = row.sourceIPAddress + "-" + row.destinationIPAddress
                transcriptionArray = []

                actual_packet_timestamp = row.flowStartMilliseconds
                previous_packet_timestamp = row.flowStartMilliseconds

                for index in range(len(row.accumulate_ipTotalLength)):
                    # print(index)
                    if index != 0:
                        previous_packet_timestamp = actual_packet_timestamp
                        actual_packet_timestamp = actual_packet_timestamp + row.accumulate_interPacketTimeMilliseconds[index-1]

                    actual_packet_length: int = row.accumulate_ipTotalLength[index]
                    actual_packet_direction: bool = row.accumulate_flowDirection[index]

                    symbol: str = TcpLenSymbolGenerator.generate(actual_packet_length, actual_packet_direction)
                    communication_gaps: list = self.communication_gaps_generator.generate(previous_packet_timestamp, actual_packet_timestamp)

                    transcriptionArray.extend(communication_gaps)
                    transcriptionArray.append(symbol)

                # iterator += 1
                # if iterator == 500000:
                #     iterator = 0
                #     self.__flush()
                #
                if key not in self.streams.keys():
                    self.streams[key] = []
                transcriptionString: str = ''.join(transcriptionArray)
                transcription: Transcription = Transcription(
                    row.flowStartMilliseconds,
                    row.flowDurationMilliseconds,
                    transcriptionString)
                self.streams[key].append(transcription)

            # self.__flush()
        return self.streams


    def __flush(self):
        StreamFlusher.flush(self.streams)
        for key in self.streams:
            self.streams[key].clear()


    # def __is_tcp_packet(self, packet: Packet):
    #     return packet.protocol_identifier == 6


    def __generate_output_symbols(self, entry, key):
        communication_gaps: list = self.communication_gaps_generator.generate(entry, self.streams_last_timestamps[key])
        symbol = TcpLenSymbolGenerator.generate(entry, key)
        self.streams[key].extend(communication_gaps)
        self.streams[key].append(symbol)
