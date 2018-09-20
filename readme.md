# importing xlsx files to the C3-cloud semantic mapper

## YAML configuration file

Please refer to the example yaml file provided

This file is used by the script to know where the data are located.
It tells it which files to load, which sheets, and which columns contain the data for the mappings to upload.

## Excel file

The structure of the xslx file is a bit flexible thanks to the YAML configuration, but some general assumptions are made:

- the very first row of each sheet shall contain the names of the different sites 
- the second row is supposed to contain additional title information (that are not used by the script)
- the third row is the first row containing mappings

- the first column shall contain the mappings designations
- each site shall be organized in three columns: 
    - first column: code system
	- second column: code
	- third column: code's designation
	
Please refer to the provided excel file for an example of what is expected.
	
## Running the script


```sh
python loaderScript.py path/to/configuration.yaml [--force]
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

