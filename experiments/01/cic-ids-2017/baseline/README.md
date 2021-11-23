# Baseline examples
This file guides you how to run experiments for the baseline models for each of the CIC-IDS 2017 days.

### Tuesday
```shell
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 5500 --HalvingGridSearchCV
```

### Wednesday
```shell
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 5000
```

### Thursday
```shell
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 20000 --HalvingGridSearchCV
```

### Friday
```shell
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 5500 --HalvingGridSearchCV
```
