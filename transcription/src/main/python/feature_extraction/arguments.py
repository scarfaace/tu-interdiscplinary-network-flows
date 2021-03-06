from argparse import ArgumentParser


class MyArgumentsParser:
    def __init__(self):
        self.argument_adders = [
            # FilepathArgument(),
            FeaturesArgument()
        ]

    def parse_arguments(self):
        parser = ArgumentParser(description="")
        for argument_adder in self.argument_adders:
            parser = argument_adder.add_argument_to_parser(parser)
        args = parser.parse_args()
        return args


# class FilepathArgument:
#     @staticmethod
#     def add_argument_to_parser(parser):
#         parser.add_argument("--filepath", type=str, required=True, nargs='+',
#                             help="File path of the network streams in csv.")
#         return parser



class FeaturesArgument:
    @staticmethod
    def add_argument_to_parser(parser):
        parser.add_argument("--features", type=str, required=True, nargs='+',
                            help="List of features.")
        return parser
