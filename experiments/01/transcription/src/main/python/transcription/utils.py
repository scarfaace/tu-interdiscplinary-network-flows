

class IpKeyUtil:
    def split_ip_key(self, ip_key: str):
        split_arr = ip_key.split(sep='-')
        return split_arr[0], split_arr[1]
