import unittest
from unittest.mock import patch, call

from transcription.output import BasicOutputPrinter


class OutputPrinterTest(unittest.TestCase):

    @patch('builtins.print')
    def test_GIVEN_dictionaryOfOneStream_WHEN_calledPrint_THEN_outputIsCorrectlyPrinted(self, mock_print):
        basicOutputPrinter = BasicOutputPrinter()
        streams = {
            '1.1.1.1 - 2.2.2.2': "AAA---ab---Cd"
        }

        basicOutputPrinter.print(streams)

        mock_print.assert_called_with('1.1.1.1 - 2.2.2.2,AAA---ab---Cd')

    @patch('builtins.print')
    def test_GIVEN_dictionaryOfMultipleStreams_WHEN_calledPrint_THEN_outputIsCorrectlyPrinted(self, mocked_print):
        basicOutputPrinter = BasicOutputPrinter()
        streams = {
            '0.0.0.0 - 1.1.1.1': 'AAA---ab---Cd',
            '1.1.1.1 - 2.2.2.2': 'AAA---ab---Cd',
            '2.2.2.2 - 3.3.3.3': 'aa--bb--CC'
        }

        basicOutputPrinter.print(streams)

        assert mocked_print.mock_calls == [
            call('0.0.0.0 - 1.1.1.1,AAA---ab---Cd'),
            call('1.1.1.1 - 2.2.2.2,AAA---ab---Cd'),
            call('2.2.2.2 - 3.3.3.3,aa--bb--CC')
        ]
