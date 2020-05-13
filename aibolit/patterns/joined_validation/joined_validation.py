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
import sys
from aibolit.types_decl import LineNumber
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from javalang.tree import BinaryOperation, ThrowStatement, IfStatement


class JoinedValidation:
    """
    Pattern which matches joined validations: validations (if with a single throw inside) which condition
    contains more than condition joined with OR
    """

    def __init__(self):
        pass

    def value(self, filename) -> List[LineNumber]:
        """
        Returns the line number of joined validations found in file.
        """

        def c1(node):
            return type(node.node.condition) == BinaryOperation

        def c2(node):
            return node.node.condition.operator == '||'

        def c3(node):
            return type(node.node.then_statement) == ThrowStatement

        def c4(node):
            return hasattr(node.node.then_statement, "statements") and len(node.node.then_statement.statements) == 1

        def c5(node):
            return type(node.node.then_statement.statements[0]) == ThrowStatement

        sys.setrecursionlimit(5000)
        return [
            node.line
            for node in JavalangImproved(filename).filter([IfStatement])
            if (c1(node) and c2(node)) and (c3(node) or (c4(node) and c5(node)))
        ]
