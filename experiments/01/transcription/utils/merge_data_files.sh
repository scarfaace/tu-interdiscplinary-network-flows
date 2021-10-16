### This script merges all CICIDS 2017 days (separate files) into one dataset


base_file_names=( "Monday" "Tuesday" "Wednesday" "Thursday" "Friday" )
file_name_postfix="_transcription_labeled"
output_file_path="../out/merged.tsv"

for base_file_name in "${base_file_names[@]}"
do
  input_file_path="../out/${base_file_name}${file_name_postfix}.tsv"

  echo "Merging file ${input_file_path} into ${output_file_path}"

  # if file exists and file size is greater than 0, then append all except of header
  # else sink the whole input file (also with the header)
  if [ -s "$output_file_path" ]
  then
    tail -n +2 "$input_file_path" >> "$output_file_path"
  else
    cat "$input_file_path" > "$output_file_path"
  fi

  echo "Finished merging"
done