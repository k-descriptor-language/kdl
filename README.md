# kdl-poc

[![Build Status](https://travis-ci.com/knime-dsl/kdl.svg?branch=master)](https://travis-ci.com/knime-dsl/kdl)

Takes input KNIME workflow called "TestWorkflow.knwf", extracts values from the CSV Reader node and generates new workflow "TestWorkflow_new.knwf" using template file

## Install dependencies
`pip3 install -r requirements.txt`

## Install package
`python3 setup.py install`

## Run
`kdlc -i TestWorkflow.knwf`

## Test
`python3 -m pytest -s`
