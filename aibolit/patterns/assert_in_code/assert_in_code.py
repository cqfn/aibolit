from typing import List

from aibolit.ast import AST, ASTNodeType, build_ast


class AssertInCode:
    def value(self, filename: str) -> List[int]:
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        nodes = tree.nodes_by_type(ASTNodeType.ASSERT_STATEMENT)
        for node in nodes:
            lines.append(tree.get_attr(node, 'source_code_line'))

        return lines
