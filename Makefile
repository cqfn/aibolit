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
	#uv pip install .
	uv run aibolit --version

test:
	uv run coverage run -m unittest discover

it:
	$(uv python find) -m test.integration.test_patterns_and_metrics
	$(uv python find) -m test.integration.test_model > /dev/null
	./test/integration/test_recommend.sh

xcop:
	xcop $$(find . -name '*.xml')

ruff:
	uv run ruff check aibolit test scripts --exclude scripts/target/*

sphinx:
	rm -rf sphinx html
	sphinx-apidoc -o sphinx aibolit --full
	sphinx-build sphinx html

mypy:
	uv run mypy aibolit

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html
