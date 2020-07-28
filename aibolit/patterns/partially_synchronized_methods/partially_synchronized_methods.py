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

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class PartiallySynchronizedMethods:
    """
    Methods and constructors must have no 'synchronized' statements at all,
    including statements in lambda functions and anonymous class methods,
    or consist of single 'synchronized' statement (fully synchronized)
    """

    def value(self, filename: str) -> List[int]:
        ast = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for method_ast in ast.get_subtrees(
            ASTNodeType.METHOD_DECLARATION, ASTNodeType.CONSTRUCTOR_DECLARATION
        ):
            method_declaration = method_ast.get_root()
            is_fully_sync_method = len(method_declaration.body) == 1 and \
                method_declaration.body[0].node_type == ASTNodeType.SYNCHRONIZED_STATEMENT

            synchronized_statements = list(
                method_ast.get_proxy_nodes(ASTNodeType.SYNCHRONIZED_STATEMENT)
            )

            if len(synchronized_statements) > 0 and not is_fully_sync_method:
                lines.extend(statement.line for statement in synchronized_statements)

        return lines
