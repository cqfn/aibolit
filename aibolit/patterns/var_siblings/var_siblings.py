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
    def _traverse_method_vars(self, ast: AST, node: ASTNode) -> Dict:
        vars_info: Dict = {}
        for local_var_node in ast.get_proxy_nodes(ASTNodeType.LOCAL_VARIABLE_DECLARATION):
            var_line = local_var_node.line
            var_declaration = list(ast.get_subtree(
                local_var_node).get_proxy_nodes(ASTNodeType.VARIABLE_DECLARATOR))[0]
            var_name = var_declaration.name
            if var_name not in vars_info:
                # to filter not complex names
                temp_name = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', var_name)
                if len(temp_name) > 1:
                    vars_info[var_name] = var_line
        return vars_info

    def _compare_nodes_names(self, node1_name: str, node2_name: str) -> bool:
        # here we want to find those names, which start with the same word
        # and the lenght of this word > 3
        node_name = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node1_name)
        if node2_name != node1_name and \
                node2_name.startswith(node_name[0]) and len(node_name[0]) > 3:
            return True
        return False

    def _find_sibling_vars(self, vars_info: Dict) -> List[int]:
        lines: List[int] = []
        for node in vars_info.keys():
            for new_node in vars_info.keys():
                if self._compare_nodes_names(node, new_node) and vars_info[new_node] not in lines:
                    lines.append(vars_info[new_node])
        return lines

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            variables_info = self._traverse_method_vars(ast, method_declaration)
            lines.extend(self._find_sibling_vars(variables_info))
        return sorted(lines)
