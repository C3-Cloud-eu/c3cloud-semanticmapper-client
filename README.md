# C3-cloud semantic mapper client updater

This package parses xlsx files containing the data for the Semantic Mapper of C3-cloud,  
and allows to visualize new/modified/outdated concepts and to upload new data to the server

## Requirements

Python 3.7

## Installation

### Github

Clone the repository and `cd` to it:

``` sh
git clone https://github.com/mikaeldusenne/c3cloud-semanticmapper-client
cd c3cloud-semanticmapper-client
```

Install the package:

```sh
python setup.py install
```

#### Virtual environment

If you do not wish to make a system-wide installation, you can use a virtual environment:

```
python -m venv VENV
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

### Docker

	
## Running the script


```sh
python -m c3cloudsis-client path/to/configuration.yaml --api-key [-k] /path/to/apikey/file --config /path/to/config.yaml  [--force] [--dry-run]
```

parameters:

> the path to the yaml configuration file.

options:

> `--force` → force overriding data on the server if the mapping already exists and is different than the one provided in the excel file


Sample running example:

```sh
python loaderScript.py ../data/import.yaml --force
```

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

