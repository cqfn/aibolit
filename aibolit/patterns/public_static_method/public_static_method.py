import javalang

from aibolit.utils.ast_builder import build_ast


class PublicStaticMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = build_ast(filename).filter(javalang.tree.MethodDeclaration)
        return [
            node.position.line for
            path, node in tree if
            all(elem in node.modifiers for elem in ['public', 'static'])
        ]
