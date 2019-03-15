# kdl-poc

[![Build Status](https://travis-ci.com/k-descriptor-language/kdl.svg?branch=master)](https://travis-ci.com/k-descriptor-language/kdl)
[![codecov](https://codecov.io/gh/k-descriptor-language/kdl/branch/master/graph/badge.svg)](https://codecov.io/gh/k-descriptor-language/kdl)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)


Takes input KNIME workflow called "TestWorkflow.knwf", extracts values from the CSV Reader node and generates new workflow "TestWorkflow_new.knwf" using template file

## Install dependencies
`pip3 install -r requirements.txt`

## Install package
`python3 setup.py install`

## Run
`kdlc -i TestWorkflow.knwf`

## Test
`python3 -m pytest -s`
