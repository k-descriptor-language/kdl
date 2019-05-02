#!/bin/bash

# ANTLR jar location
ANTLR=/usr/local/lib/antlr-4.7.2-complete.jar

# check if ANTLR installed
if [ ! -f $ANTLR ]
then
  echo "$ANTLR not found"
  echo "Please follow the installation instructions at https://www.antlr.org/"
  exit 1
fi

# clean up previous
rm -rf kdlc/parser

# generate
java -jar $ANTLR \
  -Dlanguage=Python3 \
  -o kdlc/parser \
  -Xexact-output-dir \
  -lib grammar \
  grammar/KDL.g4

touch kdlc/parser/__init__.py

echo "ANTLR parser successfully generated in kdlc/parser"
