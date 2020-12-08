import csv

from transcription.labels.KeysGenerator import LabelsFileEntryKeysGenerator


class LabelsFileLoader:
    @classmethod
    def load(cls, labels_filename) -> dict:
        labels = {}
        with open(labels_filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader)        # skip header
            for row in csv_reader:
                key = LabelsFileEntryKeysGenerator.generate_keys(row)
                labels[key] = LabelObject(row[-1], row[-2])
        return labels


class LabelObject:
    def __init__(self, label, attack):
        self.label = label
        self.attack = attack
