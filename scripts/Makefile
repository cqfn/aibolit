all: samples filter metrics

# Fetch thousands of Java samples in GitHub and store them
# all in target/01 directory. We don't filter anything at
# this stage. Just clone visible GitHub repos.
samples:
	python3 ./01-fetch-github.py

# We find all suitable Java classes in target/01 and copy
# them into target/02. The full list of all copies files will
# be stored in target/02-java-files.csv
filter:
	python3 ./02-filter-and-move.py --dir target/01

# Here we go through the list of all Java classes in target/02,
# and calculate a few metrics per each of them. The result of
# calculation we store into target/03-metrics.csv
metrics:
	python3 ./03-calculate-metrics.py

clean:
	rm -rf target

