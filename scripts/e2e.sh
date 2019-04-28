#!/bin/bash

e2e() {
  echo -n "$3-e2e test..."

  kdlc -i "examples/$1" -o output.knwf

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
}

e2e TestWorkflow.kdl TestWorkflow.kdl basic
e2e Meta.kdl Meta.kdl metanode
e2e TestWorkflowConcise.kdl TestWorkflow.kdl concise
