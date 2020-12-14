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