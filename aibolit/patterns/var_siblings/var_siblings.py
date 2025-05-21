# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re
from typing import List, Dict

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class VarSiblings:
    '''
    Find those variables, which have complex
    names and start with the same word
    '''
    def _collect_method_variables_names(self, ast: AST, node: ASTNode) -> Dict[str, int]:
        assert node.node_type == ASTNodeType.METHOD_DECLARATION
        vars_lines: Dict[str, int] = {}
        for local_var_node in ast.get_proxy_nodes(ASTNodeType.LOCAL_VARIABLE_DECLARATION):
            for var_declaration in local_var_node.declarators:
                var_name = var_declaration.name
                if var_name not in vars_lines:
                    # to filter not complex names
                    temp_name = re.split('([A-Z][^A-Z]*)', var_name)
                    if len(temp_name) > 1:
                        vars_lines[var_name] = local_var_node.line
        return vars_lines

    def _is_names_close(self, node_name_1: str, node_name_2: str) -> bool:
        # here we want to find those names, which start with the same word
        # and the lenght of this word > 3
        common_names_prefix = re.split('([A-Z][^A-Z]*)', node_name_1)[0]
        return node_name_2.startswith(common_names_prefix) and len(common_names_prefix) > 3

    def _find_sibling_vars(self, vars_info: Dict) -> List[int]:
        lines: List[int] = []
        for node_name1 in vars_info:
            for node_name2 in vars_info:
                if (node_name1 != node_name2 and
                        self._is_names_close(node_name1, node_name2) and
                        vars_info[node_name2] not in lines):
                    lines.append(vars_info[node_name2])
        return lines

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            variables_info = self._collect_method_variables_names(ast, method_declaration)
            lines.extend(self._find_sibling_vars(variables_info))
        return sorted(lines)
