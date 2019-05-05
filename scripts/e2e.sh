#!/bin/bash

e2e() {
  echo -n "$3-e2e test..."

  if [ -n "$4" ]
  then
      kdlc -i "examples/$1" -o output.knwf -tp "examples/$4" -d
  else
      kdlc -i "examples/$1" -o output.knwf
  fi

  kdlc -i output.knwf -o output.kdl

  diff "examples/$2" output.kdl > thediff
  rc=$?

  if [ $rc != 0 ] 
  then 
          echo "failed 😱"
          cat thediff 
  else
          echo "passed 👍"
  fi

  if [ -f thediff ] 
  then 
          rm thediff
  fi

  rm output.knwf
  rm output.kdl

  if [ $rc != 0 ] 
  then 
          exit "$rc" 
  fi
}

e2e TestWorkflow.kdl TestWorkflow.kdl basic
e2e Meta.kdl Meta.kdl metanode
e2e TestWorkflowConcise.kdl TestWorkflow.kdl concise
# `diff` doesn't work because of fields reordering, only manual testing for now
#e2e MetaConcise.kdl Meta.kdl metaconcise custom_templates/MetaTest
