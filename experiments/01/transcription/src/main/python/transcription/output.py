from transcription.labels.processing import LabelingService
from transcription.utils import IpKeyUtil


class BasicOutputPrinter:
    def __init__(self, ipKeyUtil: IpKeyUtil):
        self.header = '{}\t{}\t{}\t{}\t{}'.format("flowStartMilliseconds",
                                                  "flowDurationMilliseconds",
                                                  "sourceIPAddress",
                                                  "destinationIPAddress",
                                                  "transcription")
        self.ipKeyUtil = ipKeyUtil

    def print(self, streams):
        print(self.header)
        for hosts_pair_key in streams:
            ip1, ip2 = self.ipKeyUtil.split_ip_key(hosts_pair_key)
            for transcriptionObject in streams[hosts_pair_key]:
                output_line = '{}\t{}\t{}\t{}\t{}'.format(
                    int(transcriptionObject.flowStartMilliseconds),
                    int(transcriptionObject.flowDurationMilliseconds),
                    ip1,
                    ip2,
                    transcriptionObject.transcriptionString)
                print(output_line)



class LabelsOutputPrinter:
    def __init__(self, ipKeyUtil: IpKeyUtil, labelingService: LabelingService):
        self.header = 'srcIP\tdstIP\tlabel\tattack\ttranscription'
        self.ipKeyUtil = ipKeyUtil
        self.labelingService = labelingService

    def print(self, streams):
        print(self.header)
        for hosts_pair_key in streams:
            ip1, ip2 = self.ipKeyUtil.split_ip_key(hosts_pair_key)
            for transcriptionObject in streams[hosts_pair_key]:
                # start_transcription = datetime.now()
                label = self.labelingService.get_label(ip1, ip2, transcriptionObject.flowStartMilliseconds)
                # end_transcription = datetime.now()
                # print('labeling time:', (end_transcription - start_transcription).total_seconds())
                transcriptionString = transcriptionObject.transcriptionString
                output_line = '{}\t{}\t{}\t{}\t{}'.format(ip1, ip2, label.label, label.attack, transcriptionString)
                print(output_line)

    # def __find_ip_pair_in_labels(self, labels, ip1, ip2) -> LabelObject:
    #     key_format = '{}-{}'
    #     key1 = key_format.format(ip1, ip2)
    #     key2 = key_format.format(ip2, ip1)
    #     if key1 in labels:
    #         return labels[key1]
    #     if key2 in labels:
    #         return labels[key2]
    #     else:
    #         return LabelObject(None, None)
