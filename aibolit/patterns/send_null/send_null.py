from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast


class SendNull:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:

        lines = set()
        tree = AST.build_from_javalang(build_ast(filename))
        invocatios_types = [
            ASTNodeType.METHOD_INVOCATION,
            ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION,
            ASTNodeType.CLASS_CREATOR
        ]
        for node in tree.get_proxy_nodes(*invocatios_types):
            for argument in node.arguments:
                if (argument.node_type == ASTNodeType.LITERAL) and (argument.value == "null"):
                    lines.add(argument.line)

        for node in tree.get_proxy_nodes(ASTNodeType.TERNARY_EXPRESSION):
            has_ternary_true_value = hasattr(node.if_true, 'value')
            is_ternary_true_str = isinstance(node.if_true, str)
            has_ternary_false_value = hasattr(node.if_false, 'value')
            is_ternary_false_str = isinstance(node.if_false, str)
            if (has_ternary_true_value and is_ternary_true_str and node.if_true.value == 'null') or \
                    (has_ternary_false_value and is_ternary_false_str and node.if_false.value == 'null'):
                lines.add(node.line)

        lst = sorted(lines)
        return lst
