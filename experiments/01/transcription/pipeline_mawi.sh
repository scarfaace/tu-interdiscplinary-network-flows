
# Add source roots to PYTHONPATH
export PYTHONPATH=`pwd`/src/main/python/


base_file_name="${1:-201806231400}"
pcap_file_path="../../../resources/MAWI/${base_file_name}.pcap"
feature_extraction_output_file_path="out/MAWI/${base_file_name}_features.csv"
out_transcription_file_path="out/MAWI/${base_file_name}_transcription.tsv"
feature_extraction_config_path="feature_extraction/2tuple_bidi.json"

mkdir -p "out/MAWI"

echo "Processing file ${pcap_file_path}"

# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap into a tabular format (csv)"
go-flows run features "$feature_extraction_config_path" export csv "$feature_extraction_output_file_path" source libpcap "$pcap_file_path"
echo "Feature extraction finished"
echo


# 2. Transforming network flows into sentence-like transcriptions
echo "Transforming network flows into sentence-like transcriptions"
echo `date`
python3 src/main/python/transcription/main.py --filename "$feature_extraction_output_file_path" > "$out_transcription_file_path"
echo "Finished creating sentence-like transcriptions of network flows."
echo `date`
echo


echo "NTFT saved into ${out_transcription_file_path}"
echo


echo "Deleting tmp files..."
rm "$feature_extraction_output_file_path"
echo "Finished"