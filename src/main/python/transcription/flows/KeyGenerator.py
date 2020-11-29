

class TcpPacketEntryKeyGenerator:
    @classmethod
    def generate_key(cls, streams, entry):
        hosts_pair, hosts_pair_inverse = cls.generate_possible_keys(entry)
        if hosts_pair not in streams.keys() and hosts_pair_inverse not in streams.keys():
            return hosts_pair
        if hosts_pair in streams.keys():
            return hosts_pair
        if hosts_pair_inverse in streams.keys():
            return hosts_pair_inverse

    @classmethod
    def generate_possible_keys(cls, entry):
        hosts_pair = entry.ip_source + "-" + entry.ip_dest
        hosts_pair_inverse = entry.ip_dest + "-" + entry.ip_source
        return hosts_pair, hosts_pair_inverse
