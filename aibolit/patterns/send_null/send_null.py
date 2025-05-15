# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List, Any

from aibolit.ast_framework import ASTNodeType, AST


class SendNull:

    def __init__(self):
        pass

    def __is_null(self, val: Any) -> bool:
        if not hasattr(val, 'value'):
            return False
        if not isinstance(val.value, str):
            return False
        if val.value != 'null':
            return False
        return True

    def value(self, ast: AST) -> List[int]:

        lines = set()
        invocatios_types = [
            ASTNodeType.METHOD_INVOCATION,
            ASTNodeType.EXPLICIT_CONSTRUCTOR_INVOCATION,
            ASTNodeType.CLASS_CREATOR
        ]
        for node in ast.get_proxy_nodes(*invocatios_types):
            for argument in node.arguments:
                if (argument.node_type == ASTNodeType.LITERAL) and (argument.value == "null"):
                    lines.add(argument.line)

        for node in ast.get_proxy_nodes(ASTNodeType.TERNARY_EXPRESSION):
            if self.__is_null(node.if_false) or self.__is_null(node.if_true):
                lines.add(node.line)

        lst = sorted(lines)
        return lst
