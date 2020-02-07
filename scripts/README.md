To create a dataset you should do the following:

1. Collect a list of Java sample classes from GitHub:

```
$ ./scripts/01-fetch-github.py
```

The script should create `target/01/found-java-files.txt` file with the list
of all Java files found. It will also clone GitHub repositories to
`target/01/repos` directory.

2. Collect all available metrics:

```
$ ./scripts/02-calculate-metrics.py
```

The script will calculate Cyclomatic Complexity, NPath, Lines of Code
and other metrics. The result will be stored in the file
`target/02/file-metrics.csv`. It will be a CSV file with the first
column with the file path and other columns with metric values.


