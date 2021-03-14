subsample_size="${1:-7500}"

base_file_names=( "Monday" "Tuesday" "Wednesday" "Thursday" "Friday" )

for base_file_name in "${base_file_names[@]}"
do
  echo "Subsampling non-attacks from $base_file_name..."

  input_transcription_file_path="../out/${base_file_name}_transcription.tsv"
  tmp_output_file_path="../out/${base_file_name}_non-attacks.tsv"

  # extract only non-attacks to a tmp file
  awk -F '\t' '{if(NR==1 || $3==0){print $0}}' "$input_transcription_file_path" > "$tmp_output_file_path"

  # pip install subsample
  # subsample non-attacks
  subsample --header-rows=1 --sample-size "$subsample_size" "$tmp_output_file_path" > "${base_file_name}_non-attacks_subsample.tsv"

  # delete the tmp file
  rm "$tmp_output_file_path"

  echo "Finished subsampling non-attacks from $base_file_name"
done