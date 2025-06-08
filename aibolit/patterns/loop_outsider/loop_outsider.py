# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List
from aibolit.types_decl import LineNumber
from javalang import parse

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.ast_node import ASTNode


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
        with open(filename, 'r') as f:
            content = f.read()
        javalang_parsed = parse.parse(content)
        ast = AST.build_from_javalang(javalang_parsed)
        loop_types = [ASTNodeType.WHILE_STATEMENT, ASTNodeType.FOR_STATEMENT,
                      ASTNodeType.DO_STATEMENT]

        for loop_type in loop_types:
            for loop_statement in ast.get_proxy_nodes(loop_type):
                var_changes = set()
                loop_vars_declarations = set()
                subtree = ast.get_subtree(loop_statement)
                # Looking for all variable declarations
                for node in subtree.get_proxy_nodes(
                        ASTNodeType.LOCAL_VARIABLE_DECLARATION):

                    # pick only one single name
                    loop_vars_declarations.add(node.names[0])

                    # variable declaration in for (int i = 0...
                    # is considered as part of loop declaration
                if loop_type == ASTNodeType.FOR_STATEMENT:
                    for node_for in subtree.get_proxy_nodes(
                            ASTNodeType.VARIABLE_DECLARATION):
                        loop_vars_declarations.add(node_for.names[0])



                    # the looking variables which affected by any operation
                # Examining (++ --)
                for node in ast.get_proxy_nodes(ASTNodeType.MEMBER_REFERENCE):
                    if self.variableIsAffected(node):
                        var_changes.add(node)

                # NOTE: all kinds of assignments (=, +=, etc.) are considered to be
                # variable changing
                for node in ast.get_proxy_nodes(ASTNodeType.ASSIGNMENT):
                    var_changes.add(node.expressionl)


                # finally, if affected variable is not declared in loop_vars,
                # it is a pattern
                for node in var_changes:
                    if node.member not in loop_vars_declarations:
                        res.append(node.line)



        return sorted(res)

    def variableIsAffected(self, node):
        if ('--' in node.prefix_operators or '--' in node.postfix_operators or
                '++' in node.prefix_operators or '++' in
                node.postfix_operators):
            return True
        else:
            return False


if __name__ == "__main__":
    t = LoopOutsider()
    print(t.value(
        "/home/aziz/Projects/COOP/aibolit/test/patterns/loop_outsider"
        "/LoopOutsiderAddAndInWhile.java"))
