#!/bin/bash

help_run () {
  echo "Usage: pipeline-general.sh pcap_file_path"
}

pcap_file_path="${1}"
if [ -z "$pcap_file_path" ]; then
  help_run
  exit 1;
fi

# Add source roots to PYTHONPATH
export PYTHONPATH=`pwd`/src/main/python/

RANDOM_STRING=`openssl rand -hex 12 | cut -c1-6`
feature_extraction_output_file_path="out/features_${RANDOM_STRING}.csv"
out_transcription_file_path="out/transcription_${RANDOM_STRING}.tsv"

feature_extraction_config_path="feature_extraction/2tuple_bidi.json"

echo "Processing file ${pcap_file_path}"

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
