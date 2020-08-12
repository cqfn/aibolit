#!/bin/bash
aibolit check --folder ./test/integration/check/java
if [ $? -eq 2 ]
then
  echo "Failure: aibolit check has failed."
  exit 1
else
  echo "Success: aibolit check was successful"
  exit 0
fi