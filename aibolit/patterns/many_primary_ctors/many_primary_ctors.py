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
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework.ast_node import ASTNode
from typing import List, Union


class ManyPrimaryCtors(object):
    '''
    If there is more than one primary
    constructors in a class, it is
    considered a pattern
    '''
    def value(self, filename: str) -> List[int]:
        lines: List[int] = list()
        ast = AST.build_from_javalang(build_ast(filename))
        for class_declaration in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            primary_lines = self.__find_primary(ast, class_declaration.body)
            if len(primary_lines) > 1:
                lines.extend(primary_lines)
        return lines

    def __find_primary(self, ast: AST, class_body: List[ASTNode]) -> List[int]:
        lines: List[int] = []
        for node in class_body:
            if self.__check_primary(ast, node):
                lines.append(node.line)
        return lines

    def __check_primary(self, ast: AST, node: Union[ASTNode, List[ASTNode]]) -> bool:
        if isinstance(node, ASTNode) and node.node_type == ASTNodeType.CONSTRUCTOR_DECLARATION:
            for assignment in ast.get_subtree(node).get_proxy_nodes(ASTNodeType.ASSIGNMENT):
                if assignment.expressionl.node_type == ASTNodeType.THIS:
                    return True
        return False
