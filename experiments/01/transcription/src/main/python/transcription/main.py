import shutil

from transcription.arguments import MyArgumentsParser
from transcription.constants import TMP_STREAMS_FOLDER
from transcription.labels.processing import LabelsFileLoader, Labels, LabelingService
from transcription.output import BasicOutputPrinter, LabelsOutputPrinter
from transcription.processing import InputFileProcessor
from transcription.utils import IpKeyUtil


def clean_tmp_streams():
    shutil.rmtree(TMP_STREAMS_FOLDER)


if __name__ == '__main__':
    my_arguments_parser = MyArgumentsParser()
    inputFileProcessor = InputFileProcessor()
    labelsFileLoader = LabelsFileLoader()

    ipKeyUtil = IpKeyUtil()
    baseOutputPrinter = BasicOutputPrinter(ipKeyUtil)

    arguments = my_arguments_parser.parse_arguments()

    processed_streams = inputFileProcessor.process(arguments.filename)
    if arguments.labels_filename is not None:
        labels: Labels = labelsFileLoader.load(arguments.labels_filename)
        labelingService: LabelingService = LabelingService(labels)
        labelsOutputPrinter = LabelsOutputPrinter(ipKeyUtil, labelingService)
        labelsOutputPrinter.print(processed_streams)
    else:
        baseOutputPrinter.print(processed_streams)

    # clean_tmp_streams()
