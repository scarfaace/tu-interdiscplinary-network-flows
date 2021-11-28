## Directories

```
├── baseline_binary.py - python script for training and evaluation of baseline binary classification model
├── cic-ids-2017 - contains files related to the experiment on top of CIC IDS 2017 data
│   ├── baseline
│   │   ├── data - data for baseline mode
│   │   └── feature-extraction - files related to feature extraction for baseline model
│   └── obtained
│       └── data - data for obtained model
├── mawi
│   ├── baseline
│   │   └── data - data for baseline mode
│   └── obtained
│       └── data - data for obtained model
└── obtained_binary.py - python script for training and evaluation of obtained (on top of transcription data) binary classification model
```


## Obtaining results for baseline models

```shell
python3 baseline_binary.py OPTIONS
```
#### OPTIONS
- `--dataset-path` - path to the CSV dataset
- `--non-attacks-subsample-size` - integer representing how many non-attacks to subsample for the experiment
- `--HalvingGridSearchCV` - boolean flag indicating whether script should use sklearn's HalvingGridSearchCV 
for model training or a default model

#### Examples
```shell
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 5000 --HalvingGridSearchCV true
python3 baseline_binary.py --dataset-path datasets/file2.csv --non-attacks-subsample-size 3000
```

## Experiments
This file guides you how to run experiments for the baseline models for each of the CIC-IDS 2017 days.

### CIC-IDS 2017 dataset

#### Tuesday
```shell
python3 baseline_binary.py --dataset-path cic-ids-2017/baseline/data/Tuesday_labeled.csv --non-attacks-subsample-size 5500
```

#### Wednesday
```shell
python3 baseline_binary.py --dataset-path cic-ids-2017/baseline/data/Wednesday_labeled.csv --non-attacks-subsample-size 5000
```

#### Thursday
```shell
python3 baseline_binary.py --dataset-path cic-ids-2017/baseline/data/Thursday_labeled.csv --non-attacks-subsample-size 20000 --HalvingGridSearchCV true
```

#### Friday
```shell
python3 baseline_binary.py --dataset-path cic-ids-2017/baseline/data/Friday_labeled.csv --non-attacks-subsample-size 5500 --HalvingGridSearchCV true
```


### MAWI
#### 23rd June 2018, 14:00
```shell
python3 baseline_binary.py --dataset-path mawi/baseline/data/baseline_features_labeled.csv --non-attacks-subsample-size 50000 --HalvingGridSearchCV true
```



## Obtaining results for obtained models

```shell
python3 obtained_binary.py OPTIONS
```
#### OPTIONS
- `--dataset-path` - path to the TSV dataset
- `--non-attacks-subsample-size` - integer representing how many non-attacks to subsample for the experiment
- `--HalvingGridSearchCV` - boolean flag indicating whether script should use sklearn's HalvingGridSearchCV
  for model training or a default model

#### Examples
```shell
python3 obtained_binary.py --dataset-path datasets/file.tsv --non-attacks-subsample-size 5000 --HalvingGridSearchCV true
python3 obtained_binary.py --dataset-path datasets/file2.tsv --non-attacks-subsample-size 3000
```

## Experiments
This file guides you how to run experiments for the baseline models for each of the CIC-IDS 2017 days.

### CIC-IDS 2017 dataset

#### Tuesday
```shell
python3 obtained_binary.py --dataset-path cic-ids-2017/obtained/data/Tuesday_transcription_labeled.tsv --non-attacks-subsample-size 5500
```

#### Wednesday
```shell
python3 obtained_binary.py --dataset-path cic-ids-2017/obtained/data/Wednesday_transcription_labeled.tsv --non-attacks-subsample-size 5000 --HalvingGridSearchCV true
```

#### Thursday
```shell
python3 obtained_binary.py --dataset-path cic-ids-2017/obtained/data/Thursday_transcription_labeled.tsv --non-attacks-subsample-size 20000 --HalvingGridSearchCV true
```

#### Friday
```shell
python3 obtained_binary.py --dataset-path cic-ids-2017/obtained/data/Friday_transcription_labeled.tsv --non-attacks-subsample-size 5500 --HalvingGridSearchCV true
```


### MAWI
#### 23rd June 2018, 14:00
```shell
python3 obtained_binary.py --dataset-path mawi/obtained/data/transcriptions_labeled.tsv --non-attacks-subsample-size 50000 --HalvingGridSearchCV true
```
