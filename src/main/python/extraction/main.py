from csv import writer, QUOTE_ALL
from sys import stdout

from src.main.python.extraction.arguments.arguments import MyArgumentsParser

if __name__ == '__main__':
    # get packets record features from .pcap by tshark (pyshark)
    # create a sentence-like transcription from the data from the previous step

    my_arguments_parser = MyArgumentsParser()
    csv = writer(stdout, quoting=QUOTE_ALL)

    arguments = my_arguments_parser.parse_arguments()
    csv.writerow(arguments.features)


