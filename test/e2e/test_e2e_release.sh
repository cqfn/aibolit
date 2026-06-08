#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

set -euo pipefail

DIST_DIR=${1:-dist}

echo "Starting e2e release test..."

TEMP_VENV=$(mktemp -d --suffix=test-env)
echo "Testing in temporary environment: $TEMP_VENV"

cleanup() {
    rm -rf "$TEMP_VENV" test-files/
}

trap cleanup EXIT

echo "Creating fresh virtual environment with Python 3.11..."
uv venv --seed --python 3.11 "$TEMP_VENV"
# shellcheck disable=SC1091
source "$TEMP_VENV/bin/activate"

echo "Installing built package..."
python3 -m pip install "$DIST_DIR"/*.whl

echo "Verifying aibolit command..."
which aibolit > /dev/null

echo "Creating test Java file..."
mkdir -p test-files
cat > test-files/Sample.java << 'EOF'
public class Sample {
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void process() {
        if (name != null) {
            System.out.println("Name: " + name);
        }
    }
}
EOF

echo "Testing aibolit analysis..."
set +e
aibolit recommend --filenames test-files/Sample.java > /dev/null
exit_code=$?
set -e
if [ $exit_code -ne 1 ]; then
  echo "ERROR: aibolit recommend failed with exit code $exit_code"
  exit 1
fi

set +e
aibolit recommend --filenames test-files/Sample.java --format=compact > /dev/null
exit_code=$?
set -e
if [ $exit_code -ne 1 ]; then
  echo "ERROR: aibolit recommend failed with exit code $exit_code"
  exit 1
fi

echo "Testing error handling..."
set +e
aibolit recommend --filenames non-existent.java > /dev/null 2>&1
exit_code=$?
set -e
if [ $exit_code -eq 2 ]; then
  echo "Correctly handled non-existent file"
else
  echo "ERROR: Expected exit code 2 for non-existent file"
  exit 1
fi

echo "Testing help command..."
aibolit recommend --help > /dev/null

deactivate

echo "All e2e tests passed successfully"
