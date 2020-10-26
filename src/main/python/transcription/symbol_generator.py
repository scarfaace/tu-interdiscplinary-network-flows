from math import floor


class CommunicationGapsGenerator:
    @staticmethod
    def generate(entry, stream_last_time):
        time_diff = entry.timestamp - stream_last_time
        time_diff_tens_ms = floor(time_diff/0.1)
        gaps = []
        for tens_ms_inc in range(time_diff_tens_ms):
            gaps.append("-")
        return gaps


class TcpLenSymbolGenerator:
    @staticmethod
    def generate(entry):
        symbol = int(entry.tcp_len / 146)
        return symbol
