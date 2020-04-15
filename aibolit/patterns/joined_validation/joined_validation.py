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

import javalang

from typing import List
from aibolit.types_decl import LineNumber
from aibolit.patterns.var_middle.var_middle import JavalangImproved


class JoinedValidation:
    """
    Pattern which matches joined validations: validations (if with a single throw inside) which condition
    contains more than condition joined with OR
    """

    def __init__(self, file):
        self.file = file

    def value(self) -> List[LineNumber]:
        """
        Returns the line number of joined validations found in file.
        """

        return [
            node.line + 1
            for node in JavalangImproved(self.file).filter([javalang.tree.IfStatement])  # type: ignore
            if (type(node.node.condition) == javalang.tree.BinaryOperation and node.node.condition.operator == '||') \
            and (
                type(node.node.then_statement) == javalang.tree.ThrowStatement or \
                    (len(node.node.then_statement.statements) == 1 and \
                        type(node.node.then_statement.statements[0]) == javalang.tree.ThrowStatement)
            )
        ]
