from decimal import Decimal
from math import floor

from transcription.configuration import Configuration


class CommunicationGapsGenerator:
    def __init__(self):
        self.gap_symbol = '!'

    def generate(self, entry, stream_last_time):
        time_diff_ms = Decimal(str(entry.timestamp)) - Decimal(str(stream_last_time))
        # print('time_diff: {}'.format(time_diff_ms), file=sys.stderr)
        gaps_count = floor(time_diff_ms/Configuration.MILLISECONDS_PER_GAP)
        gaps = [self.gap_symbol] * gaps_count
        # print('time_diff: {}\ntime_diff_ms: {}\ntime_diff_10s_ms: {}\ngaps: {}'.format(time_diff, time_diff_ms, time_diff_tens_ms, len(gaps)), file=sys.stderr)
        return gaps


class TcpLenSymbolGenerator:
    @staticmethod
    def generate(entry, key):
        communication_direction = CommunicationDirectionDecider.decide_communication_direction(key, entry)
        if entry.tcp_len <= 2**14:   # 16 384
            symbol_offset = int(entry.tcp_len / 547)     # 16384 / 547 = 29,95
            symbol_number = communication_direction + symbol_offset
        elif entry.tcp_len <= 2**16:   # 65 536
            length_cut = entry.tcp_len - 2**14       # 2^16 - 2^14 = 49152
            symbol_offset = int(length_cut / 3277)   # 49152 / 3277 = 14,99
            symbol_number = communication_direction + 30 + symbol_offset
        else:
            symbol_number = communication_direction + 45    # use 46th character
        return chr(symbol_number)


class CommunicationDirectionDecider:
    @classmethod
    def decide_communication_direction(cls, key, entry) -> int:
        ip_left, ip_right = cls.__split_key_to_ip_addresses(key)
        if entry.ip_source == ip_left:
            return 34   # start at '"'
        if entry.ip_source == ip_right:
            return 80   # start at 'P'

    @classmethod
    def __split_key_to_ip_addresses(cls, key) -> tuple:
        split = key.split('-')
        ip_left = split[0]
        ip_right = split[1]
        return ip_left, ip_right
