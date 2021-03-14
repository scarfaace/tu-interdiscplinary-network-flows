#awk 'BEGIN {srand()} !/^$/ { if (rand() <= .01) print $0}'  > sample.txt

base_file_name="Wednesday"
input_file_path="out/${base_file_name}_transcription.tsv"

# pip install subsample
subsample --header-rows=1 --sample-size 10 "$input_file_path" > "${base_file_name}_transcription_subsample.tsv"
