# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
.SECONDARY:
SHELL := bash
VENV_DIR = .venv
XML_FILES = $(shell find . -type f -name "*.xml" | grep -v "$(VENV_DIR)")
.PHONY: all clean requirements test it install xcop flake8 pylint sphinx mypy lint

all: requirements install test it lint xcop sphinx

lint: flake8 pylint mypy

requirements:
	python3 -m pip install -r requirements.txt

install:
	python3 -m pip install .
	python3 aibolit --version

test:
	python3 -m coverage run -m unittest discover

it:
	python3 -m test.integration.test_patterns_and_metrics
	python3 -m test.integration.test_model > /dev/null
	./test/integration/test_recommend.sh

xcop:
	xcop --exclude=$(VENV_DIR) $(XML_FILES)

flake8:
	python3 -m flake8 aibolit test scripts setup.py --exclude scripts/target/*

pylint:
	python3 -m pylint aibolit test scripts setup.py --ignore=scripts/target

sphinx:
	rm -rf sphinx html
	sphinx-apidoc -o sphinx aibolit --full
	sphinx-build sphinx html

mypy:
	python3 -m mypy aibolit

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html
