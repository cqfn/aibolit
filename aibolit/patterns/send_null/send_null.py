from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast


class SendNull:

    def __init__(self):
        pass

    def __is_null(self, val):
        has_ternary_true_value = hasattr(val, 'value')
        if has_ternary_true_value:
            is_ternary_true_str = isinstance(val.value, str)
            if is_ternary_true_str:
                if val.value == 'null':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

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
            if self.__is_null(node.if_false) or self.__is_null(node.if_true):
                lines.add(node.line)

        lst = sorted(lines)
        return lst
