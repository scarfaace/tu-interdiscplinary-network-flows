from xml.etree.ElementTree import iterparse


class FeatureExtractor:

    def __init__(self, csv_output, features):
        self.csv_output = csv_output
        self.features = features

    def extract(self, document):
        for event, elem in iterparse(document, events=('start', 'end')):
            if event == 'start':
                # detect start of packet
                if elem.tag == 'packet':
                    pkt = dict()
                    for feature in self.features:
                        pkt[feature] = ''
                    elem.clear()
                    continue
                # extract feature
                if elem.tag == 'field' and elem.attrib['name'] in self.features:
                    if elem.attrib['name'] == 'timestamp':
                        pkt[elem.attrib['name']] = elem.attrib['value']
                    else:
                        pkt[elem.attrib['name']] = elem.attrib['show']
                    elem.clear()
                    continue
            # detect end of packet and write output
            if elem.tag == 'packet' and event == 'end':
                if pkt['ip.src'] and pkt['ip.dst']:
                    self.csv_output.writerow([pkt[feature] for feature in self.features])
                elem.clear()
                continue
            # clear memory
            elem.clear()
