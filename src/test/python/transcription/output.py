import unittest

from python.transcription.output import OutputPrinter


class OutputPrinterTest(unittest.TestCase):

    def GIVEN_dictionaryOfStreams_WHEN_calledPrint_THEN_outputIsCorrectlyPrinted(self):
        streams = {
            '1.1.1.1 - 2.2.2.2': "AAA---ab---Cd"
        }
        OutputPrinter.print()