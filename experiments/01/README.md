# Directories

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
python3 baseline_binary.py --dataset-path datasets/file.csv --non-attacks-subsample-size 5000 --HalvingGridSearchCV
python3 baseline_binary.py --dataset-path datasets/file2.csv --non-attacks-subsample-size 3000
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
python3 baseline_binary.py --dataset-path datasets/file.tsv --non-attacks-subsample-size 5000 --HalvingGridSearchCV
python3 baseline_binary.py --dataset-path datasets/file2.tsv --non-attacks-subsample-size 3000
```
