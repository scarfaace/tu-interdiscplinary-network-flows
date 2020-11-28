from abc import ABC, abstractmethod
from argparse import ArgumentParser


class MyArgumentsParser:
    def __init__(self):
        self.argument_adders = [
            MainFileArgument(),
            LabelsFileArgument()
        ]

    def parse_arguments(self):
        parser = ArgumentParser(description="")
        for argument_adder in self.argument_adders:
            parser = argument_adder.add_argument_to_parser(parser)
        args = parser.parse_args()
        return args


class AbstractArgument(ABC):
    @abstractmethod
    def add_argument_to_parser(self, parser):
        pass


class MainFileArgument(AbstractArgument):
    def __init__(self):
        self.argument = '--filename'

    def add_argument_to_parser(self, parser):
        parser.add_argument(
            self.argument,
            type=str,
            required=True,
            help="The name of the csv file containing information about packets."
        )
        return parser


class LabelsFileArgument(AbstractArgument):
    def __init__(self):
        self.argument = '--labels-filename'

    def add_argument_to_parser(self, parser):
        parser.add_argument(
            "--filename",
            type=str,
            required=False,
            help="The name of the csv file containing labels information about network data."
        )
        return parser
