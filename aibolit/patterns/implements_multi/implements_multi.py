import javalang

from aibolit.utils.ast_builder import build_ast


class ImplementsMultiFinder:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = build_ast(filename).filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if node.implements and (len(node.implements) > 1)]
