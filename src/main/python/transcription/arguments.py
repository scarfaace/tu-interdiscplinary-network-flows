from argparse import ArgumentParser


class MyArgumentsParser:
    def __init__(self):
        self.argument_adders = [
            MainFileArgument()
        ]

    def parse_arguments(self):
        parser = ArgumentParser(description="")
        for argument_adder in self.argument_adders:
            parser = argument_adder.add_argument_to_parser(parser)
        args = parser.parse_args()
        return args


class MainFileArgument:
    @staticmethod
    def add_argument_to_parser(parser):
        parser.add_argument("--filename", type=str, required=True,
                            help="The name of the csv file containing information about packets.")
        return parser
