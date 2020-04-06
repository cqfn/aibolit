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

import javalang.ast
import javalang.parse
import javalang.tree
from aibolit.utils.ast import AST


_OP_EQUALITY = '=='
_LT_NULL = 'null'


class NullCheck(object):
    def value(self, filename: str):
        tree = AST(filename).value()

        return self.__traverse_node(tree)

    def __traverse_node(self, tree: javalang.ast.Node):
        lines = list()

        for path, node in tree.filter(javalang.tree.BinaryOperation):
            if _is_null_check(node) and not _within_constructor(path):
                lines.append(node.operandr.position.line)

        return lines


def _is_null_check(node: javalang.ast.Node):
    return node.operator == _OP_EQUALITY and node.operandr.value == _LT_NULL


def _within_constructor(path):
    node_types = [type(p) for p in path[::2]]

    return javalang.tree.ConstructorDeclaration in node_types
