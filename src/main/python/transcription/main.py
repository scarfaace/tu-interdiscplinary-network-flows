from python.transcription.arguments import MyArgumentsParser
from python.transcription.output import OutputPrinter
from python.transcription.processing import InputFileProcessor

if __name__ == '__main__':

    my_arguments_parser = MyArgumentsParser()
    arguments = my_arguments_parser.parse_arguments()

    processed_streams = InputFileProcessor.process(arguments.filename)

    OutputPrinter.print(processed_streams)
