# KDL 

[![Build Status](https://travis-ci.com/k-descriptor-language/kdl.svg?branch=master)](https://travis-ci.com/k-descriptor-language/kdl)
[![codecov](https://codecov.io/gh/k-descriptor-language/kdl/branch/master/graph/badge.svg)](https://codecov.io/gh/k-descriptor-language/kdl)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


Takes input KNIME workflow called "TestWorkflow.knwf", extracts values from the CSV Reader node and generates new workflow "TestWorkflow_new.knwf" using template file

## Install Package
`python3 setup.py install`

## Run

```bash
❯ kdlc --help
Usage: kdlc [OPTIONS]

Options:
  -o, --output TEXT  The output file, either .knwf or .kdl  [required]
  -i, --input PATH   The input file, either .knwf or .kdl  [required]
  -m, --modify PATH  The KNIME workflow file (.knwf) being modified
  -n, --nodes PATH   The path to the custom node templates
  --help             Show this message and exit.
```

### Workflow to Workflow (development only) 
`kdlc -i TestWorkflow.knwf -o OutputWorkflow.knwf`

## Development

## Install Development Dependencies
`pip install -e '.[dev]'`

### Run Tests
`pytest --cov=./`

### Run Quality Checks
`./scripts/quality-check.sh`

### Run Formatter
`./scripts/format.sh`
