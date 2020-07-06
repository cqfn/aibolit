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
from typing import List
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast

import javalang
import re


class MethodSiblings:
    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:

        numbers = []
        for _, node in build_ast(filename).filter(javalang.tree.MethodDeclaration):
            composed = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node.name)
            if len(composed) > 1:
                for _, inner in build_ast(filename).filter(javalang.tree.MethodDeclaration):
                    if node.name != inner.name:
                        if inner.name.startswith(composed[0]):
                            numbers.append(node.position.line)
        return numbers
