<img src="/logo.png" height="92px"/>

[![PyPi version](https://img.shields.io/pypi/v/aibolit.svg)](https://pypi.org/project/aibolit/)
[![Build Status](https://travis-ci.org/yegor256/aibolit.svg)](https://travis-ci.org/yegor256/aibolit)
[![Hits-of-Code](https://hitsofcode.com/github/yegor256/aibolit)](https://hitsofcode.com/view/github/yegor256/aibolit)
[![Test Coverage](https://img.shields.io/codecov/c/github/yegor256/aibolit.svg)](https://codecov.io/github/yegor256/aibolit?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e90e80a143a9457ee3af/maintainability)](https://codeclimate.com/github/yegor256/aibolit/maintainability)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/yegor256/aibolit/blob/master/LICENSE.txt)

First, you install it (you must have [Python 3+](https://www.python.org/downloads/)
and [Pip](https://pip.pypa.io/en/stable/installing/) installed):

```bash
$ pip3 install aibolit
```

Then, you run it to analyze your Java sources, located at `src/java` (for example):

```bash
$ aibolit src/java
```

It will tell you where are the problems (if anything found).

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

If everything is fine, submit
a [pull request](https://www.yegor256.com/2014/04/15/github-guidelines.html).
