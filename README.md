## Directories

```
├── experiments - folder containing implementations and experiments provided for this research
├── labeling - folder containing labeling related resources
├── report - folder containing the project's report
├── resources - resources folder containing research papers, datasets,...
└── wiki - github wiki related resources 
```

## Create virtual environment
In order to set up an environment for development and running scripts, you have to
create a new virtual environment and install dependencies:

```shell
$ virtualenv <env_name>   # creates an environment
$ source <env_name>/bin/activate   # activates the environment
(<env_name) $ pip install -r requirements.txt    # installs dependencies
```

`<env_name>` can be any string, e.g. `venv`.


## Other dependencies

### go-flows
go-flows is used in this project to extract features from pcap files.
Outputs of go-flows are either used in the transcription making process or
for training and evaluation of baseline models.

Installation:
1. Ensure `libpcap-dev` or equivalent is installed
2. Install the go compiler: https://golang.org/doc/ install
3. Execute `go get github.com/CN-TU/go-flows` in a terminal