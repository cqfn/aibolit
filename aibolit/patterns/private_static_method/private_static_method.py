import javalang
from aibolit.utils.ast import AST


class PrivateStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = AST(filename).value().filter(javalang.tree.MethodDeclaration)
        private_static_methods = list()
        for node in [node for path, node in tree if all(elem in node.modifiers for elem in ['private', 'static'])]:
            private_static_methods.append(node.position.line)
        return private_static_methods
