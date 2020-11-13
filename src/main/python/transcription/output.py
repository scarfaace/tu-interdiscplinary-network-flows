

class OutputPrinter:
    @classmethod
    def print(cls, streams):
        for hosts_pair_key in streams:
            symbols_stream = ''.join(streams[hosts_pair_key])
            output_line = '{}: {}'.format(hosts_pair_key, symbols_stream)
            print(output_line)
