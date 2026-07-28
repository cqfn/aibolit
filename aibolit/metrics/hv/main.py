# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path


class HVMetric():
    """Main Halstead Volume class."""

    input = ''
    jar_path = Path(__file__).resolve().parents[2] / 'binary_files' / 'halstead.jar'

    def __init__(self, input):
        self.input = input

    def value(self):
        """Run Halstead Volume analysis"""
        if len(self.input) == 0:
            raise ValueError('Empty file for analysis')

        if not self.jar_path.is_file():
            raise FileNotFoundError(f'Halstead jar file not found: {self.jar_path}')
        result = subprocess.run(['java', '-jar', str(self.jar_path), self.input],
                                stdout=subprocess.PIPE, check=True)
        out = result.stdout.decode('utf-8')
        return {'data': [{'file': self.input, 'halsteadvolume': float(out)}]}
