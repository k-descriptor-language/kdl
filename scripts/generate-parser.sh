#!/bin/bash

# clean up previous
rm -rf parser

# generate
java -jar /usr/local/lib/antlr-4.7.2-complete.jar -Dlanguage=Python3 kdl.g4 -o kdlc/parser
