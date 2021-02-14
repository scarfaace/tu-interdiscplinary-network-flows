from decimal import Decimal
from math import floor


class CommunicationGapsGenerator:
    def __init__(self):
        self.gap_symbol = '!'

    def generate(self, entry, stream_last_time):
        time_diff = Decimal(str(entry.timestamp)) - Decimal(str(stream_last_time))
        time_diff_ms = time_diff * 1000
        # print('time_diff: {}'.format(time_diff_ms), file=sys.stderr)
        time_diff_tens_ms = floor(time_diff_ms/10)
        gaps = []
        for tens_ms_inc in range(time_diff_tens_ms):
            gaps.append(self.gap_symbol)
        # print('time_diff: {}\ntime_diff_ms: {}\ntime_diff_10s_ms: {}\ngaps: {}'.format(time_diff, time_diff_ms, time_diff_tens_ms, len(gaps)), file=sys.stderr)
        return gaps


class TcpLenSymbolGenerator:
    @staticmethod
    def generate(entry, communication_direction):
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
