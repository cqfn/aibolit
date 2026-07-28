# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import AST, ASTNodeType


class ClassVariable:
    """
    Find local variables declared with the same concrete class type they instantiate.
    """

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for variable_declaration in ast.proxy_nodes(ASTNodeType.LOCAL_VARIABLE_DECLARATION):
            if variable_declaration.type.node_type != ASTNodeType.REFERENCE_TYPE:
                continue

            declared_type = self._get_type_name(variable_declaration.type)
            for declarator in variable_declaration.declarators:
                initializer = declarator.initializer
                if initializer is None or initializer.node_type != ASTNodeType.CLASS_CREATOR:
                    continue

                if self._get_type_name(initializer.type) == declared_type:
                    lines.append(variable_declaration.line)
                    break
        return lines

    @staticmethod
    def _get_type_name(type_node) -> str:
        parts = [type_node.name]
        sub_type = type_node.sub_type
        while sub_type is not None:
            parts.append(sub_type.name)
            sub_type = sub_type.sub_type
        return '.'.join(parts)
