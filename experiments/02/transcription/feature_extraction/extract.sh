#pcap_file_path="../resources/CIC-IDS-2017/Tuesday-WorkingHours.pcap"
pcap_file_path="../in/test.pcap"

go-flows run features pcap2pkts.json export csv "../out/test_goflows2.csv" source libpcap "$pcap_file_path"
