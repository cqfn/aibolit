from typing import List

import javalang
from aibolit.utils.ast import AST
from aibolit.patterns.pattern import Pattern
from aibolit.types_decl import LineNumber


class ImplementsMultiFinder(Pattern):

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if node.implements and (len(node.implements) > 1)]
