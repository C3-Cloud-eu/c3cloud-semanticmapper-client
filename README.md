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
	--apikey-path data/apikey \\
	--config data/import.yaml \\
	--url 'https://rubis.limics.upmc.fr/c3-cloud/' \\
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
	--apikey-path data/apikey \\
	--config data/import.yaml \\
	--url 'https://rubis.limics.upmc.fr/c3-cloud/' \\
	[--dry-run] [--force] [--delete]
```

parameters:

> `--config` the path to the yaml configuration file.

> `--apikey-path` the path to the file containing the API key.

> `--url` url to the API

options:

> `--force` → force overriding data on the server if the mapping already exists and is different than the one provided in the excel file

> `--dry-run` → simulate import: do not perform any modification of the server data

> `--delete` → delete concepts and mapping not present in the excel sheet. Recommended to use if performing a whole-data update (i.e. the excel sheet contains the entirety of the data supposed to be on the server).



## Logs and behaviour

The script will do some output for each mapping and for each site it tries to upload.

When a mapping is identical to what is already on the server side, it will not try to upload it and the output will be:
```
already in db→ <apixaban>@<OSAKI>:[identical]
```

When a mapping already exist on the server and is different to the one provided in your xlsx file, it will print both versions to the console and will **not** override it if you did not use the `--force` option.

Here is an example where the `designation` fields differ:

```
already in db→ <pneumococcal disease vaccination>@<CDSM>:[different]
local:
['code', '12866006']
['code_system', 'SNOMED CT']
['concept', 'pneumococcal disease vaccination']
['designation', 'Pneumococcal vaccination (procedure)']
['site', 'CDSM']


server:
['code', '12866006']
['code_system', 'SNOMED CT']
['code_system_uri', 'uri:oid:2.16.840.1.113883.6.96']
['concept', 'pneumococcal disease vaccination']
['designation', 'Pneumococcal vaccination']
['site', 'CDSM']

[use --force to overwrite]
```

Lastly, when the mapping does not exist on the server side it will be uploaded.

