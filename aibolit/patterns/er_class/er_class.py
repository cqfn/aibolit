from aibolit.ast_framework import ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage
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
        ast = JavaPackage(filename)
        class_decls = list(ast.get_nodes(ASTNodeType.CLASS_DECLARATION))
        for node in class_decls:
            names = []
            class_name = ast.get_attr(node, 'name').lower()
            for n in classes:
                if n in class_name:
                    names.append(class_name)
            if names:
                lines.append(ast.get_attr(node, 'line'))
        return lines
