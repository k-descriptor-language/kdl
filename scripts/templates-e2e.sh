#!/bin/bash

echo "template-e2e test..."

kdlc -i examples/TestWorkflowConcise.kdl -o concise.knwf

kdlc -i concise.knwf -o concise.kdl

diff examples/TestWorkflow.kdl concise.kdl > thediff
rc=$?

if [ $rc != 0 ] 
then 
        cat thediff 
else
        echo "passed 👍"
fi

if [ -f thediff ] 
then 
        rm thediff
fi

rm concise.knwf
rm concise.kdl

exit "$rc"
