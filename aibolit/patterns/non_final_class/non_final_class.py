from typing import List
from javalang.tree import ClassDeclaration
from aibolit.types import LineNumber
from aibolit.utils.ast import AST


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value()
        classes = tree.filter(ClassDeclaration)
        return [
            node.position.line for _, node in classes
            if 'final' in node.modifiers
        ]
