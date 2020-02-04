#!/bin/bash
set -x
set -e

pip3 install .

pip3 install -r requirements.txt

python3 aibolit --version

coverage run -m unittest discover

python3 -m flake8 aibolit test

