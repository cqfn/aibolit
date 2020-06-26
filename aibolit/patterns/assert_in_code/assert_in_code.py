from typing import List
from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class AssertInCode:
    def value(self, filename: str) -> List[int]:
        tree = AST(build_ast(filename))
        lines = []
        nodes = tree.nodes_by_type(ASTNodeType.ASSERT_STATEMENT)
        for node in nodes:
            lines.append(tree.get_attr(node, 'source_code_line'))

        return lines
