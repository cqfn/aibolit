#!/bin/bash
set -x
set -e

pip install .

pip install -r requirements.txt

python3 aibolit --version

python3 -m unittest discover

python -m flake8 aibolit test

