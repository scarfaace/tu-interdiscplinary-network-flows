input_transcription_file_path="../out/Monday_transcription.csv"
output_file_path="../out/Monday_attacks.csv"

awk -F , '{if(NR==1 || $3==1){print $0}}' "$input_transcription_file_path" > "$output_file_path"