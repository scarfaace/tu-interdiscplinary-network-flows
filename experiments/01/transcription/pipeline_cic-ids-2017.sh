#!/bin/bash

help_run () {
  echo "Usage: pipeline_cic-ids-2017.sh day"
  echo "Examples:"
  echo -e "\t pipeline_cic-ids-2017.sh Monday"
  echo -e "\t pipeline_cic-ids-2017.sh Tuesday"
  echo -e "\t pipeline_cic-ids-2017.sh Wednesday"
  echo -e "\t pipeline_cic-ids-2017.sh Thursday"
  echo -e "\t pipeline_cic-ids-2017.sh Friday"
}

day_name="${1}"
#day_name="${1:-Thursday}"
if [ -z "$day_name" ]; then
  help_run
  exit 1;
fi

# Add source roots to PYTHONPATH
export PYTHONPATH=`pwd`/src/main/python/


pcap_file_path="../../../resources/CIC-IDS-2017/${day_name}-WorkingHours.pcap"
feature_extraction_output_file_path="out/${day_name}_features.csv"
out_transcription_file_path="out/${day_name}_transcription.tsv"
feature_extraction_config_path="feature_extraction/2tuple_bidi.json"

echo "Processing file ${pcap_file_path}"

# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap into a tabular format (csv)"
go-flows run features "$feature_extraction_config_path" export csv "$feature_extraction_output_file_path" source libpcap "$pcap_file_path"
echo "Feature extraction finished"
echo


# 2. Extracting flows as conversation transcriptions
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