

class LabelsFileEntryKeysGenerator:
    @classmethod
    def generate_keys(cls, row):
        hosts_pair = row[2] + "-" + row.ip_dest[3]
        return hosts_pair
