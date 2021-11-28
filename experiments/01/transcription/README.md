# Scripts description

## pipeline_cic-ids-2017.sh
- This script creates sentence-like transcriptions out of the specified CIC-IDS-2017 pcap file.
- Before running the script, you have to download the CIC-IDS-2017 pcap files 
\[https://www.unb.ca/cic/datasets/ids-2017.html].
  - Save these files into `resources/CIC-IDS-2017` folder located in the project root 
    and keep its original names.
- The final output transcription file will be stored in the `out/` folder.


### Run
```shell
./pipeline_cic-ids-2017.sh DAY
```
`DAY` - the data day which you want to process, one of the following values:
`Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`

### Examples
```shell
./pipeline_cic-ids-2017.sh Wednesday
./pipeline_cic-ids-2017.sh Friday
```


## pipeline_general.sh
- This script creates sentence-like transcriptions out of the specified pcap file.
- The final output transcription file will be stored in the `out/` folder.

### Run
```shell
./pipeline_general.sh PCAP_FILE_PATH
```
`PCAP_FILE_PATH` - the pcap data file to be processed

### Examples
```shell
./pipeline_general.sh ~/data/my-file.pcap
```