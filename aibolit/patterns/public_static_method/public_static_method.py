import javalang
from aibolit.utils.ast import AST


class PublicStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = AST(filename).value().filter(javalang.tree.MethodDeclaration)
        return [
            node.position.line for
            path, node in tree if
            all(elem in node.modifiers for elem in ['public', 'static'])
        ]
