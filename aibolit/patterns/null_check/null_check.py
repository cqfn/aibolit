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

from typing import List, Tuple, Type

from javalang.ast import Node
from javalang.tree import CompilationUnit, BinaryOperation, Expression, Literal, ConstructorDeclaration

from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST

Path = Tuple


_OP_EQUAL = "=="
_OP_NOT_EQUAL = "!="
_LT_NULL = "null"


class NullCheck(object):
    def value(self, filename: str) -> List[LineNumber]:
        tree: CompilationUnit = AST(filename).value()

        return self._traverse_node(tree)

    def _traverse_node(self, tree: CompilationUnit) -> List[LineNumber]:
        lines: List[LineNumber] = list()

        for path, node in tree.filter(BinaryOperation):
            if _is_null_check(node) and not _within_constructor(path):
                lines.append(node.operandr.position.line)

        return lines


def _is_null_check(node: BinaryOperation) -> bool:
    return node.operator in (_OP_EQUAL, _OP_NOT_EQUAL) and _is_null(node.operandr)


def _is_null(node: Expression) -> bool:
    return isinstance(node, Literal) and node.value == _LT_NULL


def _within_constructor(path: Path) -> bool:
    node_types: List[Type[Node]] = [type(p) for p in path[::2]]

    return ConstructorDeclaration in node_types
