<img src="/logo.svg" height="92px"/>

[![PyPi version](https://img.shields.io/pypi/v/aibolit.svg)](https://pypi.org/project/aibolit/)
[![Build Status](https://travis-ci.org/cqfn/aibolit.svg)](https://travis-ci.org/cqfn/aibolit)
[![Build status](https://ci.appveyor.com/api/projects/status/gr3eqxq5pr87kpwg?svg=true)](https://ci.appveyor.com/project/yegor256/aibolit)
[![Hits-of-Code](https://hitsofcode.com/github/cqfn/aibolit)](https://hitsofcode.com/view/github/cqfn/aibolit)
[![Test Coverage](https://img.shields.io/codecov/c/github/cqfn/aibolit.svg)](https://codecov.io/github/cqfn/aibolit?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/fd7e32d8472b4d5e8ecb/maintainability)](https://codeclimate.com/github/cqfn/aibolit/maintainability)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/cqfn/aibolit/blob/master/LICENSE.txt)

First, you install it (you must have [Python 3.7.7](https://www.python.org/downloads/)
and [Pip](https://pip.pypa.io/en/stable/installing/) installed):

```bash
$ pip3 install aibolit
```

To analyze your Java sources, located at `src/java` (for example), run:

```bash
$ aibolit check --filenames src/java/File.java src/java/AnotherFile.java
```
or

```bash
$ aibolit recommend --filenames src/java/File.java src/java/AnotherFile.java
```

Also, you can set a folder with Java files:

```bash
$ aibolit recommend --folder src/java
```

It will run recommendation function for the model (model is located in [aibolit/binary_files/model.pkl](https://github.com/cqfn/aibolit/blob/master/aibolit/binary_files/model.pkl).
The model finds a pattern which contribution is the largest to the Cyclomatic Complexity.
If anything is found, you will see all recommendations for the mentioned patterns.
You can see the list of all patterns in [Patterns.md](https://github.com/cqfn/aibolit/blob/master/PATTERNS.md).
The output of recommendation will be redirected to the stdout.
If the program has the `0` exit code, it means that all analyzed files do not have any issues.
If the program has the `1` exit code, it means that at least 1 analyzed file has an issue.
If the program has the `2` exit code, it means that program crash occurred.


You can suppress certain patterns (comma separated value) and they will be ignored. They won't be included into the report, also their importance will be set to 0.
```bash
$ aibolit recommend --folder src/java --suppress=P12,P13
```

You can change the format, using the `--format` parameter. The default value is `--format=compact`.
```bash
$ aibolit recommend --folder src/java --format=compact --full
```

It will output sorted patterns by importance in descending order and grouped by a pattern name:

```
Show all patterns
/mnt/d/src/java/Configuration.java score: 127.67642529949538
/mnt/d/src/java/Configuration.java[3840]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[3844]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[3848]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[2411]: Null Assignment (P28: 10.76 2/4)
/mnt/d/src/java/Configuration.java[826]: Many primary constructors (P9: 10.76 3/4)
/mnt/d/src/java/Configuration.java[840]: Many primary constructors (P9: 10.76 3/4)
/mnt/d/src/java/Configuration.java[829]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[841]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[865]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[2586]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3230]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3261]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3727]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3956]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/ErrorExample.java: error when calculating patterns: Can't count P1 metric:
Total score: 127.67642529949538
```

`(P21: 30.95612931128819 1/4)` means the following:


```
30.95612931128819 is the score of this pattern
1 is the position of this pattern in the total list of patterns found in the file
4 is the total number of found patterns
```

You can use `format=long`. In this case all results will be sorted by a line number:

```
Show all patterns
/mnt/d/src/java/Configuration.java: some issues found
/mnt/d/src/java/Configuration.java score: 127.67642529949538
/mnt/d/src/java/Configuration.java[826]: Many primary constructors (P9: 10.76 3/4)
/mnt/d/src/java/Configuration.java[829]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[840]: Many primary constructors (P9: 10.76 3/4)
/mnt/d/src/java/Configuration.java[841]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[865]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[2411]: Null Assignment (P28: 10.76 2/4)
/mnt/d/src/java/Configuration.java[2586]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3230]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3261]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3727]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/Configuration.java[3840]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[3844]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[3848]: Var in the middle (P21: 30.95612931128819 1/4)
/mnt/d/src/java/Configuration.java[3956]: Partial synchronized (P14: 0.228 4/4)
/mnt/d/src/java/ErrorExample.java: error when calculating patterns: Can't count P1 metric:
/mnt/d/src/java/MavenSlice.java: your code is perfect in aibolit's opinion
Total score: 127.67642529949538
```



You can also choose xml format. It will have the same format as `text` mode, but xml will be created:

```xml
<report>
  <score>127.67642529949538</score>
  <!--Show all patterns-->
  <files>
    <file>
      <path>/mnt/d/src/java/Configuration.java</path>
      <summary>Some issues found</summary>
      <score>127.67642529949538</score>
      <patterns>
        <pattern code="P13">
          <details>Null check</details>
          <lines>
            <number>294</number>
            <number>391</number>
          </lines>
          <score>30.95612931128819</score>
          <order>1/4</order>
        </pattern>
        <pattern code="P12">
          <details>Non final attribute</details>
          <lines>
            <number>235</number>
          </lines>
          <score>10.76</score>
          <order>2/4</order>
        </pattern>
          <pattern code="P21">
          <details>Var in the middle</details>
          <lines>
            <number>235</number>
          </lines>
          <score>2.056</score>
          <order>3/4</order>
        </pattern>
          <pattern code="P28">
          <details>Null Assignment</details>
          <lines>
            <number>2411</number>
          </lines>
          <score>0.228</score>
          <order>4/4</order>
        </pattern>
      </patterns>
    </file>
    <file>
      <path>/mnt/d/src/java/ErrorExample.java</path>
      <summary>Error when calculating patterns: Can't count P1 metric: </summary>
    </file>
    <file>
      <path>/mnt/d/src/java/MavenSlice.java</path>
      <summary>Your code is perfect in aibolit's opinion</summary>
    </file>
  </files>
</report>

```
The score is the relative importance of the pattern (there is no range for it).
The larger score is, the most important pattern is.
E.g., if you have several patterns, first you need to fix the pattern with the score 5.45:

```
/mnt/d/src/java/SampleTests.java[43]: Non final attribute (P12: 5.45 1/10)
/mnt/d/src/java/SampleTests.java[44]: Non final attribute (P12: 5.45 1/10)
/mnt/d/src/java/SampleTests.java[80]: Var in the middle (P21: 3.71 2/10)
/mnt/d/src/java/SampleTests.java[121]: Var in the middle (P21: 3.71 2/10)
/mnt/d/src/java/SampleTests.java[122]: Var declaration distance for 5 lines (P20_5: 2.13 3/10)
/mnt/d/src/java/SampleTests.java[41]: Non final class (P24: 1.95 4/10)
/mnt/d/src/java/SampleTests.java[59]: Force Type Casting (P5: 1.45 5/10)
/mnt/d/src/java/SampleTests.java[122]: Var declaration distance for 7 lines (P20_7: 1.07 6/10)
/mnt/d/src/java/SampleTests.java[122]: Var declaration distance for 11 lines (P20_11: 0.78 7/10)
/mnt/d/src/java/SampleTests.java[51]: Protected Method (P30: 0.60 8/10)
/mnt/d/src/java/SampleTests.java[52]: Super Method (P18: 0.35 9/10)
/mnt/d/src/java/SampleTests.java[100]: Partial synchronized (P14: 0.08 10/10)
/mnt/d/src/java/SampleTests.java[106]: Partial synchronized (P14: 0.08 10/10)
/mnt/d/src/java/SampleTests.java[113]: Partial synchronized (P14: 0.08 10/10)
```
The score per class is the sum of all patterns scores.

```
/mnt/d/src/java/SampleTests.java score: 17.54698560768407
```

The total score is an average among all java files in a project (folder you've set to analyze)
```
Total average score: 4.0801854775508914
```

If you have 2 scores of different projects, the worst project is that one which has the highest score.



Model is automatically installed with *aibolit* package, but you can also try your own model

```bash
$ aibolit recommend --folder src/java --model /mnt/d/some_folder/model.pkl
```

You can get full report with `--full` command, then all patterns will be included to the output:

```bash
$ aibolit recommend --folder src/java --full
```

You can exclude folder with `--exclude` command. The last parameter is the folder to exclude,
the rest of them are glob patterns.
```bash
$ aibolit recommend --folder src/java --exclude=**/*Test*.java --exclude=**/*Impl*.java --exclude=/mnt/d/src/java/tests
```

If you need help, run

```bash
$ aibolit recommend --help
```

## How to retrain it?

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
$ aibolit train --java_folder=src/java [--max_classes=100] [--dataset_file]
```

If you need to save the dataset with all calculated metrics to a different directory, you need to use `dataset_file` parameter

```bash
$ aibolit train --java_folder=src/java --dataset_file /mnt/d/new_dir/dataset.csv
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
  cqfn/aibolit-image
```
