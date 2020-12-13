
# Add source roots to PYTHONPATH
export PYTHONPATH=`pwd`/src/main/python/

pcap_file_path="resources/CIC-IDS-2017/Tuesday-WorkingHours.pcap"


# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap into a tabular format (csv)"
go-flows run features feature_extraction/pcap2pkts.json export csv out/Tuesday.csv source libpcap "$pcap_file_path"


# 2. Extracting flows as conversation transcriptions
echo "Extracting flows as conversation transcriptions"
python3 src/main/python/transcription/main.py --filename out/Tuesday.csv --labels-filename resources/CIC-IDS-2017/labels_CAIA_17.csv > out/Tuesday_transcription.csv
