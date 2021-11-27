## Directories

```
├── cic-ids-17 - contains CIC-IDS 2017 labeling related files 
└── mawi - contains MAWI labeling related files
```

## Labeling CIC-IDS 2017 data sets

### Baseline

```shell
python3 cic-ids-17/CICIDS17_labeling_baseline.py CSV
```
`CSV` - CSV file to be labeled

#### Output
Outputs data set with binary labels. The column `Label` indicates 
`1` for attack and `0` for non-attack


### Transcriptions
Use this script of you want to label transcriptions data set. The difference is that this
script labels TSV files and deals with `"` characters to not use them for string wrapping.

```shell
python3 cic-ids-17/CICIDS17_labeling_transcriptions.py TSV
```
`TSV` - TSV file to be labeled

#### Output
Outputs data set with binary labels. The column `Label` indicates
`1` for attack and `0` for non-attack.

---

## Labeling MAWI data sets

### Baseline
Example of a command to generate labeled baseline dataset:
```shell
python3 mawi/20180623_1400/baseline_labeling.py --baseline_no_label_path ../resources/mawi/20180623_1400/baseline_features_3M.csv  --attacks_input_path ../resources/mawi/20180623_1400/20180623_anomalous_suspicious.csv --output_labeled_baseline "./01_output.csv"
```

### Transcriptions
Example of a command to generate labeled transcription dataset:
```shell
python3 mawi/20180623_1400/transcriptions_labeling.py --transcription_no_label_path ../resources/mawi/20180623_1400/transcription_MAWI_3M.tsv --attacks_input_path ../resources/mawi/20180623_1400/20180623_anomalous_suspicious.csv --output_labeled_transcription "./01_output.tsv"
```

- `baseline_no_label_path` - path to the input, non-labeled, file
- `attacks_input_path` - path to the labeling file containing information about attacks
