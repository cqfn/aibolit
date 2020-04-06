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

import itertools
import re
from collections import namedtuple
from aibolit.utils.ast import AST

import javalang

ExceptionInfo = namedtuple('ExceptionInfo', 'func_name, catch_list, throws_list, line_number')


class RedundantCatch:

    def __init__(self):
        pass

    def value(self, filename):
        tree = AST(filename).value()
        with open(filename, encoding='utf-8') as file:
            lines_str = file.readlines()

        pattern_catch = re.compile(r'(catch[\(\s]+[\w | \s]+)')
        total_code_lines = []
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            catch_list = []
            ei = ExceptionInfo(
                func_name=method_node.name,
                catch_list=catch_list,
                throws_list=method_node.throws,
                line_number=method_node.position.line
            )
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                catch_classes = [x.parameter.types for x in try_node.catches]
                classes_exception_list = list(itertools.chain(*catch_classes))
                ei.catch_list.extend(classes_exception_list)
                catches = [
                    (i, line) for i, line in
                    enumerate(lines_str[method_node.position.line:], start=method_node.position.line)
                    if re.search(pattern_catch, line)
                ]
                code_lines = [
                    i + 1 for i, line in catches
                    if any([(line.find(y) > -1) for y in ei.throws_list])
                ]
                total_code_lines.extend(code_lines)

        return sorted(set(total_code_lines))
