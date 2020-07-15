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

from typing import Set, List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast


class ClassicSetter:

    def check_nodes(self, ast: AST, check_setter_body: List[ASTNodeType]) -> bool:
        '''
        In this function we check whether
        nodes in the function are agree with
        the definition of classic setter or not.
        Classic setter should consist of only several
        assert_statement and THIS statement.
        This statement is not-directed child of
        STATEMENT_EXPRESSION.
        '''
        suitable_nodes: List[ASTNodeType] = [
            ASTNodeType.ASSERT_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
        ]
        for node in check_setter_body:
            if node.node_type not in suitable_nodes:
                return False
        return True

    def value(self, filename: str) -> List[int]:
        lines: Set[int] = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if node.return_type is None and \
                method_name.startswith('set') and self.check_nodes(ast, node.body):
                    for child_this in ast.get_proxy_nodes(ASTNodeType.THIS):
                        child_membref = child_this.selectors
                        if len(child_membref):
                            mem_referenced_name = child_membref[0].member
                            source_line = node.line
                            if method_name.lower()[3:] == mem_referenced_name.lower():
                                lines.add(source_line)
        return sorted(list(lines))
