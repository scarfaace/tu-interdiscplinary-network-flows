from csv import writer, QUOTE_ALL
from sys import stdout, stdin

from python.feature_extraction.arguments import MyArgumentsParser
from python.feature_extraction.feature_extractor import FeatureExtractor

if __name__ == '__main__':
    # get packets record features from .pcap by tshark (pyshark)
    # create a sentence-like transcription from the data from the previous step

    my_arguments_parser = MyArgumentsParser()
    arguments = my_arguments_parser.parse_arguments()

    csv_output = writer(stdout, quoting=QUOTE_ALL)
    csv_output.writerow(arguments.features)

    feature_extractor = FeatureExtractor(csv_output, arguments.features)
    feature_extractor.extract(document=stdin)
