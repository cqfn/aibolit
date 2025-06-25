# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
import shutil
import subprocess
import tempfile
import uuid

from bs4 import BeautifulSoup


class CCMetric():
    """Main Cyclical Complexity class."""

    input = ''

    def __init__(self, input):
        """Initialize class."""
        if len(input) == 0:
            raise ValueError('Empty file for analysis')
        self.input = input

    def value(self, showoutput=False):
        """Run Cyclical Complexity analaysis"""
        try:
            root = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
            dirName = os.path.join(root, 'src/main/java')
            os.makedirs(dirName)
            if os.path.isdir(self.input):
                shutil.copytree(self.input, os.path.join(dirName, self.input))
            elif os.path.isfile(self.input):
                pos1 = self.input.rfind('/')
                os.makedirs(dirName + '/' + self.input[0:pos1])
                shutil.copyfile(self.input, os.path.join(dirName, self.input))
            else:
                raise Exception('File ' + self.input + ' does not exist')
            tmppath = os.path.dirname(os.path.realpath(__file__))
            shutil.copyfile(os.path.join(tmppath, 'pom.xml'), root + '/pom.xml')
            shutil.copyfile(os.path.join(tmppath, 'cyclical.xml'), root + '/cyclical.xml')
            if showoutput:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root, check=False)
            else:
                subprocess.run(['mvn', 'pmd:pmd'], cwd=root,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, check=False)
            if os.path.isfile(root + '/target/pmd.xml'):
                res = self.__parseFile(root)
                return res
            raise Exception('File ' + self.input + ' analyze failed')
        finally:
            shutil.rmtree(root)

    def __parseFile(self, root):
        result = {'data': [], 'errors': []}
        content = []
        with open(root + '/target/pmd.xml', 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'lxml')
            files = soup.find_all('file')
            for file in files:
                out = file.violation.string
                name = file['name']
                pos1 = name.find(root + '/src/main/java/')
                pos1 = pos1 + len(root + '/src/main/java/')
                name = name[pos1:]
                pos1 = out.find('has a total cyclomatic complexity')
                pos1 = out.find('of ', pos1)
                pos1 = pos1 + 3
                pos2 = out.find('(', pos1)
                complexity = int(out[pos1:pos2 - 1])
                result['data'].append({'file': name, 'complexity': complexity})
            errors = soup.find_all('error')
            for error in errors:
                name = error['filename']
                pos1 = name.find(root + '/src/main/java/')
                pos1 = pos1 + len(root + '/src/main/java/')
                name = name[pos1:]
                raise Exception(error['msg'])
        return result
