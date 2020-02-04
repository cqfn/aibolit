all: install requirements unittest flake8 xcop

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist

requirements:
	pip3 install -r requirements.txt

unittest:
	coverage run -m unittest discover
	python3 aibolit --version

install:
	pip3 install .

xcop:
	xcop $(find . -name '*.xml')

flake8:
	python3 -m flake8 aibolit test

