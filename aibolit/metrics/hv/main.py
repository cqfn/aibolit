# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os


class HVMetric():
    """Main Halstead Volume class."""

    input = ''

    def __init__(self, input):
        """Initialize class."""
        if len(input) == 0:
            raise ValueError('Empty file for analysis')
        self.input = input

    def value(self):
        """Run Halstead Volume analaysis"""
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                               'halsteadvolume/target/java-project-1.0-SNAPSHOT.jar'))
        if not os.path.isfile(path):
            hvpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'halsteadvolume'))
            subprocess.run(['mvn', 'clean', 'package'], cwd=hvpath)
        result = subprocess.run(['java', '-jar', path, self.input], stdout=subprocess.PIPE)
        out = result.stdout.decode('utf-8')
        res = result = {'data': [{'file': self.input, 'halsteadvolume': float(out)}]}
        return res
