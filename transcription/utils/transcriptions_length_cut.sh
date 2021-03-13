transcription_length="${1:-250000}"
echo "Cutting at ${transcription_length}th character."

base_file_name="Wednesday_transcription"
#base_file_name="Wednesday_attacks"
input_transcription_file_path="../out/""$base_file_name"".csv"
output_file_path="../out/""$base_file_name""_cut.csv"

awk -F '\t' -v transcription_length="$transcription_length" '{
  if(NR==1) {
    print $0
  } else {
    printf("%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, substr($5, 1, transcription_length));
  }
}' "$input_transcription_file_path" > "$output_file_path"