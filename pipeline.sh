
# Add source roots to PYTHONPATH
export PYTHONPATH=`pwd`/src/main/python/


# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap in a tabular format (csv)"
tshark -n -l -r test.pcap -T pdml | python3 src/main/python/feature_extraction/main.py --features timestamp ip.proto ip.src ip.dst tcp.flags tcp.len 1> out/test.csv

# 2. Extracting flows as conversation transcriptions
echo "Extracting flows as conversation transcriptions"
python3 src/main/python/transcription/main.py --filename out/test.csv --labels-filename in/test_labels.csv > out/test_tr.txt


#tshark -n -l -r test.pcap -T pdml | \
#  python3 src/main/python/feature_extraction/main.py --features timestamp ip.proto ip.src ip.dst tcp.flags tcp.len | \
#  python3 src/main/python/transcription/main.py test.csv > test_tr.txt
