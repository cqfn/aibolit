# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
.SECONDARY:
SHELL := bash
.PHONY: all clean requirements test it install xcop flake8 pylint sphinx mypy ruff style e2e build coverage

all: requirements install test it style xcop sphinx

style: flake8 pylint ruff

requirements:
	uv sync

install:
	uv pip install -e .
	uv run aibolit --version

test:
	uv run pytest --testmon --cov=aibolit/ test/

it:
	uv run python -m test.integration.test_patterns_and_metrics
	uv run python -m test.integration.test_model > /dev/null
	./test/integration/test_recommend.sh

xcop:
	while IFS= read -r f; do
		xcop "$${f}"
	done < <(find . -name '*.xml' -not -path './.venv/**' -not -path './wp/**')

flake8:
	uv run flake8 aibolit test scripts --exclude scripts/target/*

pylint:
	uv run pylint aibolit test scripts --ignore=scripts/target

ruff:
	uv run ruff check .

sphinx:
	rm -rf sphinx html
	uv run sphinx-apidoc -o sphinx aibolit --full
	uv run sphinx-build sphinx html

mypy:
	uv run mypy aibolit

build: requirements
	uv build

e2e: build
	./test/e2e/test_e2e_release.sh dist

coverage: requirements
	uv run pytest --cov aibolit --cov-report=xml

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html
