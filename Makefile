# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

-include local.mk

.PHONY: all clean requirements unittest integrationtest install xcop flake8doc typecheck

all: requirements install flake8 typecheck unittest xcop integrationtest

requirements:
	python3 -m pip install -r requirements.txt

unittest:
	python3 -m coverage run -m unittest discover
	python3 aibolit --version

integrationtest:
	python3 -m test.integration.test_patterns_and_metrics
	python3 -m test.integration.test_model
	python3 -m test.integration.test_semantic_extraction
	./test/integration/test_recommend.sh

install:
	python3 -m pip install .

xcop:
	xcop $(find . -name '*.xml')

flake8:
	python3 -m flake8 aibolit test scripts setup.py --exclude scripts/target/*

doc:
	rm -rf sphinx html
	sphinx-apidoc -o sphinx aibolit --full
	sphinx-build sphinx html

typecheck:
	python3 -m mypy aibolit

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html
