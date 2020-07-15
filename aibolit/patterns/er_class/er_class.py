from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List


class ErClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
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
        ast = AST.build_from_javalang(build_ast(filename))
        class_decls = list(ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION))
        for node in class_decls:
            names = []
            class_name = node.name.lower()
            for name in classes:
                if name in class_name:
                    names.append(class_name)
            if names:
                lines.append(node.line)
        return lines
