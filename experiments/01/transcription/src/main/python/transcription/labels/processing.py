from datetime import datetime

import pandas as pd
from pandas import DataFrame


class LabelObject:
    def __init__(self, label: int, attack: str):
        self.label = label
        self.attack = attack


class Labels:
    def __init__(self, labelsDf: DataFrame):
        self.labelsDf: DataFrame = labelsDf
        self.sourceIpCached = None
        self.destinationIpCached = None
        self.dateStartMsCached = None
        self.dateEndMsCached = None

    def get_label(self, sourceIp: str, destinationIp: str, dateStartMs: float, dateEndMs: float) -> DataFrame:
        filteredLabels: DataFrame = self.labelsDf[(self.labelsDf['sourceIPAddress'] == sourceIp) &
                                                  (self.labelsDf['destinationIPAddress'] == destinationIp) &
                                                  (self.labelsDf['flowStartMilliseconds'] >= dateStartMs) &
                                                  (self.labelsDf['flowStartMilliseconds'] <= dateEndMs)]
        return filteredLabels


class LabelsFileLoader:
    @classmethod
    def load(cls, labels_filename) -> Labels:
        labelsDf: DataFrame = pd.read_csv(labels_filename)[[
            'flowStartMilliseconds',
            'flowDurationMilliseconds',
            'sourceIPAddress',
            'destinationIPAddress',
            'Attack',
            'Label'
        ]]
        # TODO print how many rows from Friday do we have.
        #  For this purpose I can make a python notebook where I load the data, filter them and check count
        return Labels(labelsDf[labelsDf['Label'] == 1])


class LabelingService:

    def __init__(self, labelsObject: Labels):
        self.labels: Labels = labelsObject
        self.labelObject: LabelObject = None
        self.sourceIpCached: str = None
        self.destinationIpCached: str = None
        self.dateStartMsCached: int = None
        self.dateEndMsCached: int = None

    def get_label(self, sourceIp: str, destinationIp: str, flowStartMilliseconds: int) -> LabelObject:
        if not self.is_cached(sourceIp, destinationIp, flowStartMilliseconds):
            date_start_ms = self.get_date_start_in_ms_from_milliseconds(flowStartMilliseconds)
            date_end_ms = self.get_date_end_in_ms_from_milliseconds(flowStartMilliseconds)
            filteredLabels = self.labels.get_label(sourceIp, destinationIp, date_start_ms, date_end_ms)
            if 1 not in filteredLabels['Label']:
                labelObject = LabelObject(0, 'Normal')
            else:
                filteredAttacks: DataFrame = filteredLabels[(filteredLabels['Label'] == 1)]
                attackName: str = filteredAttacks['Attack'].iloc[0]
                labelObject = LabelObject(1, attackName)
            self.cache_data(labelObject, sourceIp, destinationIp, date_start_ms, date_end_ms)
        return self.labelObject


    def is_cached(self, sourceIp: str, destinationIp: str, flowStartMilliseconds: int):
        date_start_ms = self.get_date_start_in_ms_from_milliseconds(flowStartMilliseconds)
        date_end_ms = self.get_date_end_in_ms_from_milliseconds(flowStartMilliseconds)
        return sourceIp == self.sourceIpCached and \
               destinationIp == self.destinationIpCached and \
               date_start_ms == self.dateStartMsCached and \
               date_end_ms == self.dateEndMsCached


    def get_date_start_in_ms_from_milliseconds(self, milliseconds: int):
        dt = datetime.fromtimestamp(milliseconds/1000)
        return datetime(dt.year, dt.month, dt.day, 0, 0, 0).timestamp() * 1000


    def get_date_end_in_ms_from_milliseconds(self, milliseconds: int):
        dt = datetime.fromtimestamp(milliseconds/1000)
        return datetime(dt.year, dt.month, dt.day, 23, 59, 59).timestamp() * 1000

    def cache_data(self, labelObject: LabelObject, sourceIp: str, destinationIp: str, date_start_ms: float, date_end_ms: float):
        self.labelObject = labelObject
        self.sourceIpCached = sourceIp
        self.destinationIpCached = destinationIp
        self.dateStartMsCached = date_start_ms
        self.dateEndMsCached = date_end_ms
