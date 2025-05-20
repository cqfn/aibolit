# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
.SECONDARY:
SHELL := bash
.PHONY: all clean requirements test it install xcop ruff sphinx mypy lint

all: requirements install test it lint xcop sphinx

lint: ruff mypy

requirements:
	uv sync --all-extras

install:
	uv pip install .
	python3 aibolit --version

test:
	python3 -m coverage run -m unittest discover

it:
	python3 -m test.integration.test_patterns_and_metrics
	python3 -m test.integration.test_model > /dev/null
	./test/integration/test_recommend.sh

xcop:
	xcop $$(find . -name '*.xml')

ruff:
	python3 -m ruff check aibolit test scripts --exclude scripts/target/*

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
