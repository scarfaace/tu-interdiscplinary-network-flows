# TCP/IP communication flows into sentence-like transcriptions
### Research Question
Design a suitable symbolic schema that transforms TCP/IP flows into sentence-like transcriptions
and evaluate its suitability for knowledge discovery and (ideally) attack detection.

---

Get familiar with the following repo: https://github.com/CN-TU/py_pcap2transcription

Flow extractor: https://github.com/CN-TU/go-flows

---

1-page project outline: https://www.overleaf.com/project/5fb786ec59a7beec1c00b0a2

---

## pcap to NTFT transformartion

In `src/main/test/resources/test1.csv` there is a small testing file which represents output from the feature extraction
script and this goes to the transcription script.

To run transcription script with these data, run the following while located in the root directory of the project
```
export PYTHONPATH=`pwd`/src/main/
python3 src/main/python/transcription/main.py --filename src/test/resources/test1.csv > test_tr.txt
````

Mind that the `export` of `PYTHONPATH` is very important to be able to include the python project's local modules.


---

go-flows uses IANA features - https://www.iana.org/assignments/ipfix/ipfix.xml



---

## IP Packet Size

[O'Reilly](https://www.oreilly.com/library/view/internet-core-protocols/1565925726/re04.html#:~:text=The%20minimum%20size%20of%20an,maximum%20size%20is%2065%2C535%20bytes.&text=In%20the%20capture%20shown%20in,is%20set%20to%2060%20bytes.)
states the following:
- the minimum size of an IP packet is 21 bytes (20 bytes for header and 1 byte of data),
- the maximum size of an IP packet is 65 535 bytes

Based on this information, we can provide a new transcription scheme. The printable characters in ASCII start with
the character `!` (with decimal code 33) and ends at the character `~` (with decimal code 126).

Therefore, we can use the character `!` as a character denoting 10ms pause in a communication and other characters
can be used for denoting lengths of IP (or TCP) packets. We may try out a technique that will not longer distinguish
between the communication directions (it is not even properly working now). Therefore, the direction if the packet
will not longer be anyhow distinguished.


---


## Releases

[comment]: <> (### v0.0.1)

[comment]: <> (- just ASCII characters ranging from the character `!` &#40;dec code 33&#41; to the character `~` &#40;dec code 126&#41;,)

[comment]: <> (- `!` is used as character for representing 10ms gap,)

[comment]: <> (- therefore 94 characters are available for encoding packet length,)

[comment]: <> (    - we use 70 of them for encoding length <= 16 384)

[comment]: <> (    - and remaining 23 for encoding length > 16 384)

[comment]: <> (- no communication direction distinction)


### v1.0.0
- just ASCII characters ranging from the character `!` (dec code 33) to the character `~` (dec code 125),
- `!` is used as character for representing 10ms gap,
- therefore 92 characters are available for encoding packet length,
  - chars from position 34 to 125 (46 + 46) for deciding **communication direction**
- we use 46 of them for encoding the ip packet length for one direction
- and the remaining 46 to encode the other direction
- for each direction we use first 30 to encode length <= 16 384
- 15 characters for encoding length (16 384, 65 536] 
- and the last remaining character is used for packets bigger than 65 536

---

[comment]: <> (## TODO)

[comment]: <> (- make visualizations for the packet size in time for each flow)

[comment]: <> (- make a model for a numeric vector &#40;e.g. AGM&#41; so that I can compare it with the bag of words model)

[comment]: <> (---)

## Available Scripts

### pipeline.sh
- the script `pipeline.sh` creates NTFT out of the specified pcap file
- mind that right now the `pipeline.sh` script is tailored for processing CI IDS C2017 data as well as
  labeling them (attacks/non-attack) but it can be easily adjusted, i.e. use different pcap file argument
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
./pipeline.sh ./in/test.pcap
```

in order to convert a test pcap file `/transcription/in/test.pcap` into NTFT.
You will find the output TSV file in `/transcription/out/` as described in the section
about [pipeline-general.sh](#pipeline-generalsh)