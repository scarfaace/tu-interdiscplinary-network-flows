input_transcription_file_path="../out/Wednesday_attacks.csv"
output_file_path="../out/Wednesday_attacks_lengths.csv"

awk -F '\t' '{
  if(NR==1) {
    print $0
  } else {
    printf("%s\t%s\t%s\t%s\t%d\n", $1, $2, $3, $4, length($5));
  }
}' "$input_transcription_file_path" > "$output_file_path"