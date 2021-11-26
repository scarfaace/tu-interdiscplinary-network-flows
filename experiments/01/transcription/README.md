# TCP/IP communication flows into sentence-like transcriptions
### Research Question
Design a suitable symbolic schema that transforms TCP/IP flows into sentence-like transcriptions
and evaluate its suitability for knowledge discovery and (ideally) attack detection.

---

Get familiar with the following repo: https://github.com/CN-TU/py_pcap2transcription

Flow extractor: https://github.com/CN-TU/go-flows

---

1-page project outline: https://www.overleaf.com/project/5fb786ec59a7beec1c00b0a2


--------------------------

## Available Scripts

### pipeline.sh
- the script `pipeline.sh` creates NTFT out of the specified pcap file
- mind that right now the `pipeline.sh` script is tailored for processing CIC IDS 2017 data as well as
  labeling them (attacks/non-attack)
- how to run:
  - extract CIC IDS 2017 dataset labels `/transcription/resources/CIC-IDS-2017/labels_CAIA_17.csv.gz` into `transcription/resources/CIC-IDS-2017/labels_CAIA_17.csv`
  - download any pcap day data from http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/PCAPs/ and save it into 
    the folder `/transcription/resources/CIC-IDS-2017` with its original name (e.g. `Monday-WorkingHours.pcap`)
  - navigate to the `transcription` folder in the root directory 
  - run `pipeline.sh` with the 1st parameter as the name of the day that you downloaded and the script will fill in everything else
  - examples: 
    - `./pipeline.sh Monday`
    - `./pipeline.sh Tuesday`
  - after the run is finished, you can find your final output NTFT files in `/transcription/out/`


### pipeline-general.sh

- `pipeline-general.sh` allows you to run the whole pcap to NTFT pipeline with your defined input pcap file
- just run pipeline-general.sh script with the 1st argument specifying the path to your pcap file
- example: `./pipeline.sh /home/myuser/test.pcap`
- the final output NTFT file will be stored in `/transcription/out/` folder

---

## Examples

While located in `/transcription` directory, run

```shell
./pipeline-general.sh ./in/test.pcap
```

in order to convert a test pcap file `/transcription/in/test.pcap` into NTFT.
You will find the output TSV file in `/transcription/out/` as described in the section
about [pipeline-general.sh](#pipeline-generalsh)