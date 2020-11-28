from transcription.arguments import MyArgumentsParser
from transcription.output import OutputPrinter
from transcription.processing import InputFileProcessor

if __name__ == '__main__':

    my_arguments_parser = MyArgumentsParser()
    arguments = my_arguments_parser.parse_arguments()

    inputFileProcessor = InputFileProcessor()
    processed_streams = inputFileProcessor.process(arguments.filename)

    OutputPrinter.print(processed_streams)
