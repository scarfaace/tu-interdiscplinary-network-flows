base_file_names=( "Monday" "Tuesday" "Wednesday" "Thursday" "Friday" )

for base_file_name in "${base_file_names[@]}"
do
  echo "Extracting attacks from $base_file_name..."

  input_transcription_file_path="../out/${base_file_name}_transcription.tsv"
  output_file_path="../out/${base_file_name}_attacks.tsv"

  awk -F '\t' '{if(NR==1 || $3==1){print $0}}' "$input_transcription_file_path" > "$output_file_path"

  echo "Finished attacks extraction from $base_file_name"
done