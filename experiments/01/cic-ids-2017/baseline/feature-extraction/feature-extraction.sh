#!/bin/bash

help_run () {
  echo "Usage: feature-extraction.sh day"
  echo "Examples:"
  echo -e "\t feature-extraction.sh Monday"
  echo -e "\t feature-extraction.sh Tuesday"
  echo -e "\t feature-extraction.sh Wednesday"
  echo -e "\t feature-extraction.sh Thursday"
  echo -e "\t feature-extraction.sh Friday"
}

pcap_file_path="${1}"
if [ -z "$pcap_file_path" ]; then
  help_run
  exit 1;
fi

base_file_name="${1}"
pcap_file_path="../../../../../resources/CIC-IDS-2017/${base_file_name}-WorkingHours.pcap"
feature_extraction_output_file_path="../data/${base_file_name}.csv"
feature_extraction_config_path="./2tuple_bidi.json"

echo "Processing file ${pcap_file_path}"

# 1. Extracting features from pcap in a tabular format (csv)
echo "Extracting features from pcap into a tabular format (csv)"
go-flows run features "$feature_extraction_config_path" export csv "$feature_extraction_output_file_path" source libpcap "$pcap_file_path"
echo "Feature extraction finished"
echo
