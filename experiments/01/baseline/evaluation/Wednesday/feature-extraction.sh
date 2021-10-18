
base_file_name="Wednesday"
pcap_file_path="../../../../../resources/CIC-IDS-2017/${base_file_name}-WorkingHours.pcap"
feature_extraction_output_file_path="./${base_file_name}.csv"
feature_extraction_config_path="./2tuple_bidi.json"

echo "Processing file ${pcap_file_path}"

# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap into a tabular format (csv)"
go-flows run features "$feature_extraction_config_path" export csv "$feature_extraction_output_file_path" source libpcap "$pcap_file_path"
echo "Feature extraction finished"
echo
