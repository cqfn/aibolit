[![PyPi version](https://img.shields.io/pypi/v/aibolit.svg)](http://badge.fury.io/yegor256/aibolit)
[![Build Status](https://travis-ci.org/yegor256/aibolit.svg)](https://travis-ci.org/yegor256/aibolit)
[![Hits-of-Code](https://hitsofcode.com/github/yegor256/aibolit)](https://hitsofcode.com/view/github/yegor256/aibolit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/yegor256/aibolit/blob/master/LICENSE.txt)

Aibolit is Java code static analyzer with Machine Learning.

First, you install it (you must have [Python3+](https://www.python.org/downloads/)
and [pip](https://pip.pypa.io/en/stable/installing/) installed):

```bash
$ pip3 install aibolit
```

Then, you run it to analyze your Java sources, located at `src/java` (for example):

```bash
$ aibolit src/java
```

It will tell you where are the problems (if anything found).
