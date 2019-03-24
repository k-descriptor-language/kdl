#!/bin/bash

# clean up previous
rm -rf kdlc/parser

# generate
java -jar /usr/local/lib/antlr-4.7.2-complete.jar \
  -Dlanguage=Python3 \
  -o kdlc/parser \
  -Xexact-output-dir \
  -lib grammar \
  grammar/KDL.g4
