input_transcription_file_path="../out/Wednesday_transcription.csv"
output_file_path="../out/Wednesday_attacks.csv"

awk -F '\t' '{if(NR==1 || $3==1){print $0}}' "$input_transcription_file_path" > "$output_file_path"