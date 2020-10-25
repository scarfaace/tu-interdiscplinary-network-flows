import csv

from python.transcription.arguments import MyArgumentsParser


if __name__ == '__main__':

    my_arguments_parser = MyArgumentsParser()
    arguments = my_arguments_parser.parse_arguments()

    # print("kokot " + arguments.filename)

    with open(arguments.filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            print(', '.join(row))
