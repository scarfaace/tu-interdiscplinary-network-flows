# TCP/IP communication flows into sentence-like transcriptions
### Research Question
Design a suitable symbolic schema that transforms TCP/IP flows into sentence-like transcriptions
and evaluate its suitability for knowledge discovery and (ideally) attack detection.

---

Get familiar with the following repo: https://github.com/CN-TU/py_pcap2transcription

Flow extractor: https://github.com/CN-TU/go-flows

---

1-page project outline: https://www.overleaf.com/project/5fb786ec59a7beec1c00b0a2

--

## Run Manual Tests

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

### v0.0.1
- just ASCII characters ranging from the character `!` (dec code 33) to the character `~` (dec code 126),
- `!` is used as character for representing 10ms gap,
- therefore 93 characters are available for encoding packet length,
  - we use 70 of them for encoding length <= 16 384
  - and remaining 23 for encoding length > 16 384
- no communication direction distinction