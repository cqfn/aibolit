from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List


class ErClass:
    forbiden_words_in_class_names = (
        'manager',
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

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for node in list(ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION)):
            names = []
            class_name = node.name.lower()
            if any(forbiden_word in class_name for forbiden_word in self.forbiden_words_in_class_names):
                names.append(class_name)
            if names:
                lines.append(node.line)
        return lines
