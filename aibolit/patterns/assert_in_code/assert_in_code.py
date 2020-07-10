from typing import List

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType


class AssertInCode:
    def value(self, filename: str) -> List[int]:
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        nodes = tree.get_nodes(ASTNodeType.ASSERT_STATEMENT)
        for node in nodes:
            lines.append(tree.get_attr(node, 'line'))

        return lines
