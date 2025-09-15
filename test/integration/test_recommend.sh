#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

python3 -m aibolit recommend --folder ./test/integration/check/java

if [ $? -eq 2 ]; then
  echo "Failure: aibolit recommend has failed."
  exit 1
fi

echo "Success: aibolit recommend was successful"
