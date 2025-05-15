# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List

from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.ast_node import ASTNode


class RedundantCatch:
    '''
    To check wether the method throws same as it does inside the
    try -> catch structure in this method
    '''

    def _is_redundant(self, method_throw_name: List[str], try_node: ASTNode) -> bool:
        assert try_node.node_type == ASTNodeType.TRY_STATEMENT
        for catch_node in try_node.catches:
            for catch_node_name in catch_node.parameter.types:
                if catch_node_name in method_throw_name:
                    return True
        return False

    def _get_lambda_try_nodes(self, ast: AST, lambda_node: ASTNode) -> List[int]:
        assert lambda_node.node_type == ASTNodeType.LAMBDA_EXPRESSION
        return [try_node.line for try_node in
                ast.get_subtree(lambda_node).get_proxy_nodes(ASTNodeType.TRY_STATEMENT)]

    def value(self, ast: AST) -> List[int]:
        lines: List[int] = []
        excluded_nodes: List[int] = []

        for method_declaration in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION,
                                                      ASTNodeType.CONSTRUCTOR_DECLARATION):
            method_throw_names = method_declaration.throws
            for try_node in ast.get_subtree(method_declaration).get_proxy_nodes(
                    ASTNodeType.TRY_STATEMENT):
                if method_throw_names is not None and \
                        try_node.catches is not None and \
                        self._is_redundant(method_throw_names, try_node):
                    lines.append(try_node.line)

            for lambda_node in ast.get_subtree(method_declaration).get_proxy_nodes(
                    ASTNodeType.LAMBDA_EXPRESSION):
                excluded_nodes.extend(self._get_lambda_try_nodes(ast, lambda_node))
        return sorted(list(set(lines).difference(set(excluded_nodes))))
