# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re
from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class MethodSiblings:
    '''
    Count those methods, which
    start with the same names
    '''
    def _is_method_names_close(self, node: ASTNode, new_node: ASTNode) -> bool:
        splited_name = re.split('([A-Z][^A-Z]*)', node.name)
        return len(splited_name) > 1 and new_node.name.startswith(splited_name[0])

    def value(self, ast: AST) -> List[int]:
        numbers: List[int] = []
        method_nodes = ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION)

        for node in method_nodes:
            for new_node in method_nodes:
                if (node.node_index < new_node.node_index and
                        self._is_method_names_close(node, new_node)):
                    numbers.extend([node.line, new_node.line])
        return sorted(list(set(numbers)))
