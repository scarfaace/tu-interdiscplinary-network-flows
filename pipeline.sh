
# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap in a tabular format (csv)"
tshark -n -l -r test.pcap -T pdml | src/main/python/extraction/main.py --features timestamp ip.proto ip.src ip.dst tcp.flags tcp.len 1> test.csv

# 2. Extracting flows as conversation transcriptions
echo "Extracting flows as conversation transcriptions"
perl symboltran_lt.pl test.csv > test_tr.txt
