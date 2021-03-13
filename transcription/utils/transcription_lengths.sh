base_file_name="Wednesday_transcription"
input_transcription_file_path="../out/""$base_file_name"".csv"
output_file_path="../out/""$base_file_name""_lengths.csv"

awk -F '\t' '{
  if(NR==1) {
    print $0
  } else {
    printf("%s\t%s\t%s\t%s\t%d\n", $1, $2, $3, $4, length($5));
  }
}' "$input_transcription_file_path" > "$output_file_path"