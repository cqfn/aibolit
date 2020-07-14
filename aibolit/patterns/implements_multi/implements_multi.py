from typing import List

from aibolit.ast_framework.ast import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class ImplementsMultiFinder:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for node in tree.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            if node.implements and len(node.implements) > 1:
                lines.append(node.line)
        return lines
