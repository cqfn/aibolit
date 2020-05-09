from typing import List

import javalang
from aibolit.utils.ast import AST
from aibolit.patterns.pattern import Pattern
from aibolit.types_decl import LineNumber


class ErClass(Pattern):

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        classes = ('manager',
                   'controller',
                   'router',
                   'dispatcher',
                   'printer',
                   'writer',
                   'reader',
                   'parser',
                   'generator',
                   'renderer',
                   'listener',
                   'producer',
                   'holder',
                   'interceptor')
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if [n for n in classes if n in node.name.lower()] != []]
