base_file_name="Wednesday"
input_transcription_file_path="../out/${base_file_name}_transcription.tsv"
output_file_path="../out/${base_file_name}_attacks.tsv"

awk -F '\t' '{if(NR==1 || $3==1){print $0}}' "$input_transcription_file_path" > "$output_file_path"