import javalang
from aibolit.utils.ast import AST


class ProtectedMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        return [
            node.position.line
            for _, node in AST(filename).value().filter(javalang.tree.MethodDeclaration)
            if all(elem in node.modifiers for elem in ['protected'])
        ]
