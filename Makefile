# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.ONESHELL:
.SHELLFLAGS := -e -o pipefail -c
.SECONDARY:
SHELL := bash
.PHONY: all clean requirements test it install xcop flake8 pylint bandit sphinx mypy lint e2e build coverage ruff ty

all: requirements install test it lint sphinx

lint: flake8 pylint mypy ruff bandit ty xcop

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
	done < <(find . \( -path './.venv' -o -path './.env' -o -path './wp' \) -prune -o -name '*.xml' -type f -print)

flake8:
	uv run flake8 aibolit test scripts --exclude scripts/target/*

pylint:
	uv run pylint aibolit test scripts --ignore=scripts/target

bandit:
	uv run bandit -c pyproject.toml -r aibolit -ll

ruff:
	uv run ruff check .

ty:
	uvx ty==0.0.1-alpha.8 check

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
