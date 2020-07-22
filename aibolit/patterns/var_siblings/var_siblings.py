# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List, Dict
from aibolit.ast_framework.ast_node import ASTNode
import re


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
                if node_name1 != node_name2 and \
                   self._is_names_close(node_name1, node_name2) and vars_info[node_name2] not in lines:
                    lines.append(vars_info[node_name2])
        return lines

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            variables_info = self._collect_method_variables_names(ast, method_declaration)
            lines.extend(self._find_sibling_vars(variables_info))
        return sorted(lines)
