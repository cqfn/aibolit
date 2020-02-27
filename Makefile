all: requirements install unittest flake8 xcop

clean:
	rm -rf build
	rm -rf aibolit.egg-info
	rm -rf dist
	rm -rf sphinx html

requirements:
	python3 -m pip install -r requirements.txt
	sudo gem install xcop

unittest:
	python3 -m coverage run -m unittest discover
	python3 aibolit --version

install:
	python3 -m pip install .

xcop:
	xcop $(find . -name '*.xml')

flake8:
	python3 -m flake8 aibolit test scripts setup.py

doc:
	rm -rf sphinx html
	sphinx-apidoc -o sphinx aibolit --full
	sphinx-build sphinx html

