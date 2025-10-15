# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import subprocess
import os


class HVMetric():
    """Main Halstead Volume class."""

    input = ''

    def __init__(self, input: str) -> None:
        self.input = input

    def value(self) -> dict:
        """Run Halstead Volume analaysis"""
        if len(self.input) == 0:
            raise ValueError('Empty file for analysis')

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                               'halsteadvolume/target/java-project-1.0-SNAPSHOT.jar'))
        if not os.path.isfile(path):
            hvpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                                  'halsteadvolume'))
            subprocess.run(['mvn', 'clean', 'package'], cwd=hvpath, check=True)
        result = subprocess.run(['java', '-jar', path, self.input],
                                stdout=subprocess.PIPE, check=True)
        out = result.stdout.decode('utf-8')
        res = {'data': [{'file': self.input, 'halsteadvolume': float(out)}]}
        return res
