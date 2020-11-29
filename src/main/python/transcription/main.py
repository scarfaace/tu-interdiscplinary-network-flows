from transcription.arguments import MyArgumentsParser
from transcription.labels.processing import LabelsFileLoader
from transcription.output import BaseOutputPrinter, LabelsOutputPrinter
from transcription.processing import InputFileProcessor

if __name__ == '__main__':
    my_arguments_parser = MyArgumentsParser()
    inputFileProcessor = InputFileProcessor()
    labelsFileLoader = LabelsFileLoader()
    labelsOutputPrinter = LabelsOutputPrinter()

    arguments = my_arguments_parser.parse_arguments()

    processed_streams = inputFileProcessor.process(arguments.filename)
    if arguments.labels_filename is not None:
        loaded_labels = labelsFileLoader.load(arguments.labels_filename)
        labelsOutputPrinter.print(loaded_labels, processed_streams)
    else:
        BaseOutputPrinter.print(processed_streams)

