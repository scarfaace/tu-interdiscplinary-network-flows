from decimal import Decimal
from math import floor


class CommunicationGapsGenerator:
    @staticmethod
    def generate(entry, stream_last_time):
        time_diff = Decimal(str(entry.timestamp)) - Decimal(str(stream_last_time))
        time_diff_ms = time_diff * 1000
        # print('time_diff: {}'.format(time_diff_ms), file=sys.stderr)
        time_diff_tens_ms = floor(time_diff_ms/10)
        gaps = []
        for tens_ms_inc in range(time_diff_tens_ms):
            gaps.append("-")
        # print('time_diff: {}\ntime_diff_ms: {}\ntime_diff_10s_ms: {}\ngaps: {}'.format(time_diff, time_diff_ms, time_diff_tens_ms, len(gaps)), file=sys.stderr)
        return gaps


class TcpLenSymbolGenerator:
    @staticmethod
    def generate(entry, communication_direction):
        symbol_number = int(entry.tcp_len / 146 + communication_direction)
        return chr(symbol_number)
