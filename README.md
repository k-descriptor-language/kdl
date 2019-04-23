# KDL 

[![Build Status](https://travis-ci.com/k-descriptor-language/kdl.svg?branch=master)](https://travis-ci.com/k-descriptor-language/kdl)
[![codecov](https://codecov.io/gh/k-descriptor-language/kdl/branch/master/graph/badge.svg)](https://codecov.io/gh/k-descriptor-language/kdl)
[![Documentation Status](https://readthedocs.org/projects/kdl/badge/?version=latest)](https://kdl.readthedocs.io/en/latest/?badge=latest)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

K Descriptor Language serves as a domain specific language for authoring and manipulating KNIME workflows.

[Documentation](https://kdl.readthedocs.io/en/latest/?badge=latest)

## Install Package
`python3 setup.py install`

## Run

```bash
❯ kdlc --help
Usage: kdlc [OPTIONS]

Options:
  -o, --output TEXT  The output file, either .knwf or .kdl  [required]
  -i, --input PATH   The input file, either .knwf or .kdl  [required]
  --help             Show this message and exit.
```

## Development

### Install Development Dependencies
`pip install -e '.[dev]'`

### Run Tests
`pytest --cov=./`

### Run Quality Checks
`./scripts/quality-check.sh`

### Run Formatter
`./scripts/format.sh`

### Build Documentation
`./scripts/build-docs.sh`
