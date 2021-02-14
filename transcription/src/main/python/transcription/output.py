from transcription.TmpStreamReader import TmpStreamReader
from transcription.labels.processing import LabelObject




class BasicOutputPrinter:
    def __init__(self):
        self.header = 'ipPair\ttranscription'

    def print(self, streams):
        print(self.header)
        for hosts_pair_key in streams:
            symbols_stream = TmpStreamReader.read_stream_from_file(hosts_pair_key)
            output_line = '{}\t{}'.format(hosts_pair_key, symbols_stream)
            print(output_line)



class LabelsOutputPrinter:
    def __init__(self):
        self.header = 'srcIP\tdstIP\tlabel\tattack\ttranscription'

    def print(self, labels, streams):
        print(self.header)
        for hosts_pair_key in streams:
            ip1, ip2 = self.__split_ip_key(hosts_pair_key)
            label = self.__find_ip_pair_in_labels(labels, ip1, ip2)
            symbols_stream = TmpStreamReader.read_stream_from_file(hosts_pair_key)
            output_line = '{}\t{}\t{}\t{}\t{}'.format(ip1, ip2, label.label, label.attack, symbols_stream)
            print(output_line)


    def __find_ip_pair_in_labels(self, labels, ip1, ip2) -> LabelObject:
        key_format = '{}-{}'
        key1 = key_format.format(ip1, ip2)
        key2 = key_format.format(ip2, ip1)
        if key1 in labels:
            return labels[key1]
        if key2 in labels:
            return labels[key2]
        else:
            return LabelObject(None, None)


    def __split_ip_key(self, ip_key: str):
        split_arr = ip_key.split(sep='-')
        return split_arr[0], split_arr[1]
