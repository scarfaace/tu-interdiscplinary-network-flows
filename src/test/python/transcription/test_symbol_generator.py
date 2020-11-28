import unittest

from transcription.processing import TcpPacket
from transcription.symbol_generator import CommunicationGapsGenerator


class CommunicationGapsGeneratorTest(unittest.TestCase):

    def test_GIVEN_streamEntryAndStreamOccurrenceOfPreviousEntry_WHEN_calledGenerate_THEN_correctNumberOfDashesGenerated(self):
        entry = TcpPacket(
            timestamp=100.1,
            ip_protocol=6,
            ip_source="1.1.1.1",
            ip_dest="2.2.2.2",
            tcp_flags="",
            tcp_len=20
        )
        stream_last_time = 100

        gaps = CommunicationGapsGenerator.generate(entry, stream_last_time)

        self.assertEqual(10, len(gaps))
        [self.assertEqual('-', symbol) for symbol in gaps]


# class TcpLenSymbolGenerator:
#     @staticmethod
#     def generate(entry):
#         symbol = int(entry.tcp_len / 146)
#         return symbol
