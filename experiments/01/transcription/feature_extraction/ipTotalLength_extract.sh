
day="Friday"
pcap_file_path="../../../../resources/CIC-IDS-2017/${day}-WorkingHours.pcap"

go-flows run features ipTotalLength.json export csv "${day}_ipTotalLength.csv" source libpcap "$pcap_file_path"
