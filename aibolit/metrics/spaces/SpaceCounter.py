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

from statistics import variance
import re


class SpacesCounter:

    def __init__(self):
        pass

    def remove_comments(self, string):
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "",
                        string)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        string = re.sub(re.compile(r"//.*?\n"), "",
                        string)
        return string

    def __file_to_tokens(self, filename: str):
        """
        Takes path to java class file and returns tokens

        :param filename: file name
        :return: list of counted spaces
        """
        with open(filename, encoding='utf-8') as file:
            text = self.remove_comments(file.read())
            lines = []
            for x in text.splitlines():
                line = x.replace('\n', '').replace('\t', '    ')
                if line:
                    lines.append(line)

        return lines

    def value(self, filename: str):
        lines = self.__file_to_tokens(filename)
        spaces_per_line = []
        prev_left = 0
        prev_right = len(lines[0])
        for i, line in enumerate(lines):
            first_non_space_symbol_pos = len(line) - len(line.lstrip(' '))
            spaces_per_line.append(
                [i,
                 # count the difference between the position of first symbol in cur string and
                 # the position of first symbol of previous string
                 first_non_space_symbol_pos - prev_left,
                 # count the difference between the position of last symbol in cur string and
                 # the position of last symbol of previous string
                 len(line) - prev_right
                 ])
            prev_left = first_non_space_symbol_pos
            prev_right = len(line)

        left_space_variance = variance([x[1] for x in spaces_per_line])
        right_space_variance = variance([x[2] for x in spaces_per_line])
        max_left_space_diff = max([abs(x[1]) for x in spaces_per_line])
        max_right_space_diff = max([abs(x[2]) for x in spaces_per_line])
        return [left_space_variance, right_space_variance,
                max_left_space_diff, max_right_space_diff]
