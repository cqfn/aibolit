# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
.SECONDARY:
SHELL := bash
.PHONY: all clean requirements test it install xcop flake8 pylint sphinx mypy lint e2e build

all: requirements install test it lint xcop sphinx

lint: flake8 pylint mypy

requirements:
	python3 -m pip install -r requirements.txt

install:
	python3 -m pip install .
	python3 aibolit --version

test:
	python3 -m pytest --cov=aibolit/ test/

it:
	python3 -m test.integration.test_patterns_and_metrics
	python3 -m test.integration.test_model > /dev/null
	./test/integration/test_recommend.sh

xcop:
	while IFS= read -r f; do
		xcop "$${f}"
	done < <(find . -name '*.xml' -not -path './.venv/**' -not -path './wp/**')

flake8:
	python3 -m flake8 aibolit test scripts --exclude scripts/target/*

pylint:
	python3 -m pylint aibolit test scripts --ignore=scripts/target

ruff:
	python3 -m ruff check .

sphinx:
	rm -rf sphinx html
	sphinx-apidoc -o sphinx aibolit --full
	sphinx-build sphinx html

mypy:
	python3 -m mypy aibolit

build:
	python3 -m build

e2e: build
	./test/e2e/test_e2e_release.sh

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html
