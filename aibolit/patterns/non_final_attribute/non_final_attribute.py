
from typing import List

from javalang.tree import FieldDeclaration

from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST


class NonFinalAttribute:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value().filter(FieldDeclaration)

        return [node.position.line for path, node in tree if 'final' not in node.modifiers]
