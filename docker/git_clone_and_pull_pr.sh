#!/bin/bash

echo "Fetch Aibolit sources"

DEFAULT_BRANCH=master
export PULL_ID
export GIT_BRANCH

GIT_BRANCH=${GIT_BRANCH:-$DEFAULT_BRANCH}

is_pull_id () [[ -n $PULL_ID ]]

if [ -z ${PULL_ID+x} ]; then echo "PULL_ID is unset."; else echo "PULL_ID is set to '$PULL_ID'"; fi

git clone --single-branch --branch $GIT_BRANCH https://github.com/yegor256/aibolit
cd aibolit
is_pull_id && git pull --no-edit origin pull/$PULL_ID/head
pip install -e .
mkdir -p ./scripts/target