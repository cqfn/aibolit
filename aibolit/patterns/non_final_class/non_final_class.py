from typing import List
from javalang.tree import ClassDeclaration

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = build_ast(filename)
        classes = tree.filter(ClassDeclaration)
        return [
            node.position.line for _, node in classes
            if len([v for v in ['final', 'abstract'] if v in node.modifiers]) == 0
        ]
