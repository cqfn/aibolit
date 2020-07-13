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

from typing import List
from networkx import DiGraph, dfs_labeled_edges  # type: ignore

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.scope_status import ScopeStatus, ScopeStatusFlags


class VarMiddle:
    '''
    Returns lines in the file where variables declared in the middle
    of the method
    '''

    def value(self, filename):
        ast = AST.build_from_javalang(build_ast(filename))
        scope_status = ScopeStatus()
        lines_with_error: List[LineNumber] = []
        for _, destination, edge_type in dfs_labeled_edges(ast.tree, ast.root):
            if edge_type == 'forward':
                VarMiddle._on_entering_node(destination, ast.tree, scope_status, lines_with_error)
            elif edge_type == 'reverse':
                VarMiddle._on_leaving_node(destination, ast.tree, scope_status)

        return lines_with_error

    @staticmethod
    def _on_entering_node(node: int, ast: DiGraph, scope_status: ScopeStatus,
                          lines_with_error: List[LineNumber]):
        node_type = ast.nodes[node]['node_type']

        # if the variable is declared mark it and check the scope
        if node_type in VarMiddle._var_declaration_node_types:
            scope_status.add_flag(ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE)
            if ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT not in scope_status.get_status():
                lines_with_error.append(ast.nodes[node]['line'])

        # mark scope for super constructor calling
        elif node_type == ASTNodeType.STATEMENT_EXPRESSION:
            children_types = {ast.nodes[child]['node_type'] for child in ast.succ[node]}
            if ASTNodeType.SUPER_CONSTRUCTOR_INVOCATION in children_types:
                scope_status.add_flag(ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE)

        # mark scope for annotation usage
        elif node_type == ASTNodeType.ANNOTATION:
            scope_status.add_flag(ScopeStatusFlags.INSIDE_ANNOTATION_SUBTREE)

        else:
            # if we are not calling super constructor or declaring a variable
            # and node type not in black list spoil the scope
            if len(scope_status.get_status() & VarMiddle._ignore_scope_statuses) == 0 and \
               node_type not in VarMiddle._ignore_node_types:
                scope_status.remove_flag(ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT)

            if node_type in VarMiddle._new_scope_node_types:
                scope_status.enter_new_scope()

    @staticmethod
    def _on_leaving_node(node: int, ast: DiGraph, scope_status: ScopeStatus):
        node_type = ast.nodes[node]['node_type']

        # on the end of variable declaration remove according flag
        if node_type in VarMiddle._var_declaration_node_types:
            scope_status.remove_flag(ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE)

        # on the end of super constructor call remove according flag
        elif node_type == ASTNodeType.STATEMENT_EXPRESSION:
            children_types = {ast.nodes[child]['node_type'] for child in ast.succ[node]}
            if ASTNodeType.SUPER_CONSTRUCTOR_INVOCATION in children_types:
                scope_status.remove_flag(ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE)

        # on the end of annotation remove according flag
        elif node_type == ASTNodeType.ANNOTATION:
            scope_status.remove_flag(ScopeStatusFlags.INSIDE_ANNOTATION_SUBTREE)

        elif node_type in VarMiddle._new_scope_node_types:
            scope_status.leave_current_scope()

    _new_scope_node_types = {
        ASTNodeType.METHOD_DECLARATION,
        ASTNodeType.IF_STATEMENT,
        ASTNodeType.FOR_STATEMENT,
        ASTNodeType.SWITCH_STATEMENT,
        ASTNodeType.TRY_STATEMENT,
        ASTNodeType.DO_STATEMENT,
        ASTNodeType.WHILE_STATEMENT,
        ASTNodeType.BLOCK_STATEMENT,
        ASTNodeType.CATCH_CLAUSE,
        ASTNodeType.SYNCHRONIZED_STATEMENT,
    }

    _var_declaration_node_types = {
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ASTNodeType.TRY_RESOURCE,
    }

    _ignore_node_types = {
        ASTNodeType.FORMAL_PARAMETER,
        ASTNodeType.REFERENCE_TYPE,
        ASTNodeType.BASIC_TYPE,
        ASTNodeType.CATCH_CLAUSE_PARAMETER,
        ASTNodeType.ANNOTATION,
        ASTNodeType.TYPE_ARGUMENT,
        ASTNodeType.COLLECTION,
        ASTNodeType.STRING,
    }

    _ignore_scope_statuses = {
        ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE,
        ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE,
        ScopeStatusFlags.INSIDE_ANNOTATION_SUBTREE,
    }
