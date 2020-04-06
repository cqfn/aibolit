import javalang
from aibolit.utils.ast import AST


class ImplementsMultiFinder:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if node.implements and (len(node.implements) > 1)]
