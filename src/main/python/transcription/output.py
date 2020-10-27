

class OutputPrinter:
    @classmethod
    def print(cls, streams):
        for hosts_pair_key in streams:
            output_line = '{}: {}'.format(hosts_pair_key, streams[hosts_pair_key])
            print(output_line)
