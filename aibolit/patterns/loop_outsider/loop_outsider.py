# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


from typing import List, Set
from javalang import parse
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.types_decl import LineNumber


class LoopOutsider:
    """
    Pattern which matches loop outsiders: when we modify a variable which is declared outside of the
    scope of the loop.
    """

    def __init__(self):
        pass

    def value(self, filename) -> List[LineNumber]:
        """
        Returns the line number of loop outsiders found in file.
        """
        res = []
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        javalang_parsed = parse.parse(content)
        ast = AST.build_from_javalang(javalang_parsed)
        loop_types = [ASTNodeType.WHILE_STATEMENT, ASTNodeType.FOR_STATEMENT,
                      ASTNodeType.DO_STATEMENT]

        for loop_type in loop_types:
            for loop_statement in ast.get_proxy_nodes(loop_type):
                var_changes = self._find_variable_changes(ast)
                loop_vars_declarations = (
                    self._find_loop_variable_declarations(ast, loop_statement,
                                                          loop_type))

                # Check if affected variables are not declared in loop_vars
                for node in var_changes:
                    if node.member not in loop_vars_declarations:
                        res.append(node.line)

        return sorted(res)

    def _find_variable_changes(self, ast: AST) -> Set:
        """Find all variables that are modified in the code."""
        var_changes = set()

        # Find variables affected by increment/decrement operations
        for node in ast.get_proxy_nodes(ASTNodeType.MEMBER_REFERENCE):
            if self.variableIsAffected(node):
                var_changes.add(node)

        # Find variables affected by assignments
        for node in ast.get_proxy_nodes(ASTNodeType.ASSIGNMENT):
            var_changes.add(node.expressionl)

        return var_changes

    def _find_loop_variable_declarations(self, ast: AST, loop_statement,
                                         loop_type) -> Set:
        """Find all variable declarations within the loop scope."""
        loop_vars_declarations = set()
        subtree = ast.get_subtree(loop_statement)

        # Find local variable declarations
        for node in subtree.get_proxy_nodes(
                ASTNodeType.LOCAL_VARIABLE_DECLARATION):
            loop_vars_declarations.add(node.names[-1])

        # For for-loops, also check variable declarations in the loop header
        if loop_type == ASTNodeType.FOR_STATEMENT:
            for node_for in subtree.get_proxy_nodes(
                    ASTNodeType.VARIABLE_DECLARATION):
                loop_vars_declarations.add(node_for.names[-1])

        return loop_vars_declarations

    def variableIsAffected(self, node):
        return ('--' in node.prefix_operators or '--' in
                node.postfix_operators or
                '++' in node.prefix_operators or '++' in
                node.postfix_operators)
