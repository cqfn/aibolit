#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
# SPDX-License-Identifier: MIT

python3 -m aibolit check --folder ./test/integration/check/java

if [ $? -eq 2 ]; then
  echo "Failure: aibolit check has failed."
  exit 1
fi

echo "Success: aibolit check was successful"
