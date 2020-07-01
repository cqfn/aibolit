from typing import List

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST.build_from_javalang(build_ast(filename))
        nodes = tree.nodes_by_type(ASTNodeType.CLASS_DECLARATION)

        positions = []
        for node in nodes:
            line = tree.get_attr(node, 'source_code_line')
            modifiers = tree.get_attr(node, 'modifiers')

            if len([v for v in ['final', 'abstract'] if v in modifiers]) == 0:
                positions.append(line)

        return positions
