from decimal import Decimal
from math import floor

from transcription.configuration import Configuration


class CommunicationGapsGenerator:
    def __init__(self):
        self.gap_symbol = '!'

    def generate(self, previous_packet_timestamp, actual_packet_timestamp):
        time_diff_ms = Decimal(str(previous_packet_timestamp)) - Decimal(str(actual_packet_timestamp))
        # print('time_diff: {}'.format(time_diff_ms), file=sys.stderr)
        gaps_count = floor(time_diff_ms/Configuration.MILLISECONDS_PER_GAP)
        gaps = [self.gap_symbol] * gaps_count
        # print('time_diff: {}\ntime_diff_ms: {}\ntime_diff_10s_ms: {}\ngaps: {}'.format(time_diff, time_diff_ms, time_diff_tens_ms, len(gaps)), file=sys.stderr)
        return gaps


class TcpLenSymbolGenerator:
    @staticmethod
    def generate(packet_length: int, packet_direction: bool):
        communication_direction = CommunicationDirectionDecider.decide_communication_direction(packet_direction)
        if packet_length <= 2**14:   # 16 384
            symbol_offset = int(packet_length / 547)     # 16384 / 547 = 29,95
            symbol_number = communication_direction + symbol_offset
        elif packet_length <= 2**16:   # 65 536
            length_cut = packet_length - 2**14       # 2^16 - 2^14 = 49152
            symbol_offset = int(length_cut / 3277)   # 49152 / 3277 = 14,99
            symbol_number = communication_direction + 30 + symbol_offset
        else:
            symbol_number = communication_direction + 45    # use 46th character
        return chr(symbol_number)


class CommunicationDirectionDecider:
    @classmethod
    def decide_communication_direction(cls, packet_direction: bool) -> int:
        if packet_direction is True:
            return 34   # start at '"'
        else:
            return 80   # start at 'P'

    @classmethod
    def __split_key_to_ip_addresses(cls, key) -> tuple:
        split = key.split('-')
        ip_left = split[0]
        ip_right = split[1]
        return ip_left, ip_right
