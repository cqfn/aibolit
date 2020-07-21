import javalang

from aibolit.utils.ast_builder import build_ast


class PrivateStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        return [
            node.position.line
            for _, node in build_ast(filename).filter(javalang.tree.MethodDeclaration)
            if all(elem in node.modifiers for elem in ['private', 'static'])
        ]
