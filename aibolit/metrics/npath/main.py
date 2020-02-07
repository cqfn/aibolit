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
import shutil
from bs4 import BeautifulSoup
import tempfile
import uuid


class NPathMetric():
    """Main NPath Complexity class."""

    input = ''

    def __init__(self, input):
        """Initialize class."""
        if len(input) == 0:
            raise ValueError('Empty file for analysis')
        self.input = input

    def value(self, showoutput=False):
        """Run NPath Complexity analaysis"""
        try:
            root = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
            dirName = os.path.join(root, 'src/main/java')
            os.makedirs(dirName)
            if os.path.isdir(self.input):
                shutil.copytree(self.input, os.path.join(dirName, self.input))
            elif os.path.isfile(self.input):
                pos1 = self.input.rfind('/')
                os.makedirs('{}{}{}'.format(dirName, '/', self.input[0:pos1]))
                shutil.copyfile(self.input, os.path.join(dirName, self.input))
            else:
                raise Exception(' '.join(['File', self.input, 'does not exist']))
            tmppath = os.path.dirname(os.path.realpath(__file__))
            shutil.copyfile(os.path.join(tmppath, 'pom.xml'), '{}{}'.format(root, '/pom.xml'))
            shutil.copyfile(os.path.join(tmppath, 'npath.xml'), '{}{}'.format(root, '/npath.xml'))
            if showoutput:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root)
            else:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            if os.path.isfile('{}{}'.format(root, '/target/pmd.xml')):
                res = self.__parseFile(root)
                return res
            raise Exception(' '.join(['File', self.input, 'analyze failed']))
        finally:
            shutil.rmtree(root)

    def __parseFile(self, root):
        result = {'data': [], 'errors': []}
        content = []
        with open('{}{}'.format(root, '/target/pmd.xml'), 'r') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'lxml')
            files = soup.find_all('file')
            for file in files:
                out = file.violation.string
                name = file['name']
                pos1 = name.find('{}{}'.format(root, '/src/main/java/'))
                pos1 = pos1 + len('{}{}'.format(root, '/src/main/java/'))
                name = name[pos1:]
                s = 'NPath complexity of '
                pos1 = out.find(s)
                pos1 = pos1 + len(s)
                complexity = int(out[pos1:])
                result['data'].append({'file': name, 'complexity': complexity})
            errors = soup.find_all('error')
            for error in errors:
                name = error['filename']
                pos1 = name.find('{}{}'.format(root, '/src/main/java/'))
                pos1 = pos1 + len('{}{}'.format(root, '/src/main/java/'))
                name = name[pos1:]
                raise Exception(error['msg'])
        return result
