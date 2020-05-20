<img src="/logo.svg" height="92px"/>

[![PyPi version](https://img.shields.io/pypi/v/aibolit.svg)](https://pypi.org/project/aibolit/)
[![Build Status](https://travis-ci.org/yegor256/aibolit.svg)](https://travis-ci.org/yegor256/aibolit)
[![Build status](https://ci.appveyor.com/api/projects/status/1k7q7eumnhia0e3a?svg=true)](https://ci.appveyor.com/project/yegor256/aibolit)
[![Hits-of-Code](https://hitsofcode.com/github/yegor256/aibolit)](https://hitsofcode.com/view/github/yegor256/aibolit)
[![Test Coverage](https://img.shields.io/codecov/c/github/yegor256/aibolit.svg)](https://codecov.io/github/yegor256/aibolit?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e90e80a143a9457ee3af/maintainability)](https://codeclimate.com/github/yegor256/aibolit/maintainability)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/yegor256/aibolit/blob/master/LICENSE.txt)

First, you install it (you must have [Python 3.7.7](https://www.python.org/downloads/)
and [Pip](https://pip.pypa.io/en/stable/installing/) installed):

```bash
$ pip3 install aibolit
```

### Recommend command

To analyze your Java sources, located at `src/java` (for example), run:

```bash
$ aibolit recommend --filenames src/java/File.java src/java/AnotherFile.java
```

Also, you can set a folder with Java files:

```bash
$ aibolit recommend --folder src/java
```

It will run recommendation function for the model (model is located in [aibolit/binary_files/model.pkl](https://github.com/yegor256/aibolit/blob/master/aibolit/binary_files/model.pkl). 
The model finds a pattern which contribution is the largest to the Cyclomatic Complexity. 
If anything is found, you will see all recommendations for the mentioned patterns. 
You can see the list of all patterns in [Patterns.md](https://github.com/yegor256/aibolit/blob/master/PATTERNS.md).
The output of recommendation will be saved to the `out.xml` file into the current directory.
You can change the output file, using the `--output` parameter.

Model is automatically installed with *aibolit* package, but you can also try your own model

```bash
$ aibolit recommend --folder src/java --model_file /mnt/d/some_folder/model.pkl
```

You can get full report with `--full_report` command, then all patterns will be included to the output:

```bash
$ aibolit recommend --folder src/java --full_report
```

If you need help, run 

```bash
$ aibolit recommend --help
```

### Train command
`Train` command does the following:

 - Calculates patterns and metrics
 - Creates a dataset
 - Trains model and save it 
 
 Train works only with cloned git repository.
 1. Clone aibolit repository 
 2. Go to `cloned_aibolit_path`
 3. Run `pip install .`
 4. Set env variable `export HOME_AIBOLIT=cloned_aibolit_path` (example for Linux).
 5. If you need to set up own directory where model will be saved, set up also `SAVE_MODEL_FOLDER` environment variable.
 Otherwise model will be saved into `cloned_aibolit_path/aibolit/binary_files/model.pkl`
 6. If you need to set up own folder with Java files, use `--java_folder parameter`, the default value will be `scripts/target/01` of aibolit cloned repo
 7. You need to install Java 13 and Maven
 
 Or you can use our docker image (link will be soon here)
 
 Run train pipeline:

```bash
$ aibolit train --java_folder=src/java [--max_classes=100]
```

## How to contribute?

First, you need to install:

  * [Python 3+](https://www.python.org/downloads/)
  * [Pip](https://pip.pypa.io/en/stable/installing/)
  * Ruby 2.6+
  * [Xcop](https://github.com/yegor256/xcop)

Install the following packages if you don't have :

```bash
$ apt-get install ruby-dev libz-dev libxml2
```

Then, you fork the repo and make the changes. Then, you make
sure the build is still clean, by running:

```bash
$ make
```

To build white paper:
```bash
$ cd wp
$ latexmk -c && latexmk -pdf wp.tex
```

If everything is fine, submit
a [pull request](https://www.yegor256.com/2014/04/15/github-guidelines.html).


Using Docker recommendation pipeline
```bash
$ docker run --rm -it \
  -v <absolute_path_to_folder_with_classes>:/in \
  -v <absolute_path_to_out_dir>:/out \
  yegor256/aibolit-image
```
