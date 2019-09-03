[![Build Status](https://travis-ci.org/mikaeldusenne/c3cloud-semanticmapper-client.svg?branch=master)](https://travis-ci.org/mikaeldusenne/c3cloud-semanticmapper-client)

# C3-cloud semantic mapper client updater

This package parses xlsx files containing the data for the Semantic Mapper of C3-cloud,  
and allows to visualize new/modified/outdated concepts and to upload new data to the server

## Requirements

Python 3.7 ([Instructions for Mac OSX](https://docs.python-guide.org/starting/install3/osx/))


## Installation

### Docker

pull the container:

```sh
docker pull mikaeldusenne/c3cloudsis_client
```

running it requires to mount the directory containing the required informations:

```sh
docker run -v /absolute/path/to/data/folder:/app/data \\
	mikaeldusenne/c3cloudsis_client \\
	python -m c3cloud_semanticmapper_client \\
	--config ./data/import.yaml \\
	--dry-run
```

where `/absolute/path/to/data/folder` contains the data to import (i.e. the `import.yaml` file and the excel sheet to load) and the `apikey` file containing the key to authorize requests in the API.

### Github

Clone the repository and `cd` to it:

``` sh
git clone https://github.com/mikaeldusenne/c3cloud-semanticmapper-client
cd c3cloud-semanticmapper-client
```

Install the package:

```sh
python3 setup.py install
```

#### Virtual environment (optional)

If you do not wish to make a system-wide installation, you can use a virtual environment:

```
python3 -m venv VENV
```

To activate the virtual environment, run (before installing or using the package) :

```
source VENV/bin/activate
```

You should then see a `(VENV)` at the beginning of your shell prompt.

To disable the virtual environment once you are done using the package, run:

```
source ~/.bash_profile
```

to source your regular shell configuration.

	
## Running the script


```sh
python -m c3cloud_semanticmapper_client \\
	--config data/import.yaml \\
	[--url 'https://rubis.limics.upmc.fr/c3-cloud/'] \\
	[--dry-run] [--force] [--delete]
```

parameters:

> `--config` the path to the yaml configuration file.

options:

> `--url` url to the API

> `--force` → force overriding data on the server if the mapping already exists and is different than the one provided in the excel file

> `--dry-run` → simulate import: do not perform any modification of the server data

> `--delete` → delete concepts and mapping not present in the excel sheet. Recommended to use if performing a whole-data update (i.e. the excel sheet contains the entirety of the data supposed to be on the server).

## Documentation

refer to <https://rubis.limics.upmc.fr/c3-cloud/documentation/> for a more detailed description of the semantic mapper and this client.
