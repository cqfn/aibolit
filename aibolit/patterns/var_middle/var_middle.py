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

from typing import List, Callable
from functools import reduce

import javalang
from javalang.ast import Node

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast
from aibolit.utils.scope_status import ScopeStatus, ScopeStatusFlags


class VarMiddle:
    '''
    Returns lines in the file where variables declared in the middle
    of the method
    '''

    def value(self, filename):
        ast = build_ast(filename)
        return VarMiddle._traverse_tree(ast)

    @staticmethod
    def _traverse_tree(node: Node, scope_status=ScopeStatus()) -> List[LineNumber]:
        node_type = type(node)
        children = VarMiddle._get_node_children(node)
        cleanup_procedures: List[Callable[[], None]] = []
        lines_with_error: List[LineNumber] = []

        if node_type in VarMiddle._var_declaration_node_types:
            scope_status.add_flag(ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE)
            cleanup_procedures.append(
                lambda: scope_status.remove_flag(ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE))

            if ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT not in scope_status.get_status():
                lines_with_error.append(node.position.line)
        else:
            if node_type == javalang.tree.StatementExpression and \
               javalang.tree.SuperConstructorInvocation in map(type, children):
                scope_status.add_flag(ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE)
                cleanup_procedures.append(
                    lambda: scope_status.remove_flag(
                        ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE))

            if len(scope_status.get_status() & VarMiddle._ignore_scope_statuses) == 0 and \
               node_type not in VarMiddle._ignore_node_types:
                scope_status.remove_flag(ScopeStatusFlags.ONLY_VARIABLE_DECLARATIONS_PRESENT)

            if node_type in VarMiddle._new_scope_node_types:
                scope_status.enter_new_scope()
                cleanup_procedures.append(lambda: scope_status.leave_current_scope())

        for child in children:
            lines_with_error.extend(
                VarMiddle._traverse_tree(child, scope_status))

        for cleanup_procedure in cleanup_procedures:
            cleanup_procedure()

        return lines_with_error

    @staticmethod
    def _get_node_children(node: Node) -> List[Node]:
        def flatter(flat_children_list: List[Node], elem: Node) -> List[Node]:
            if isinstance(elem, list):
                flat_children_list.extend(
                    filter(lambda child: isinstance(child, Node), elem))
            elif isinstance(elem, Node):
                flat_children_list.append(elem)
            return flat_children_list

        return reduce(flatter, node.children, [])

    _new_scope_node_types = \
        {
            javalang.tree.MethodDeclaration,
            javalang.tree.IfStatement,
            javalang.tree.ForStatement,
            javalang.tree.SwitchStatement,
            javalang.tree.TryStatement,
            javalang.tree.DoStatement,
            javalang.tree.WhileStatement,
            javalang.tree.BlockStatement,
            javalang.tree.CatchClause,
            javalang.tree.SynchronizedStatement,
        }

    _var_declaration_node_types = \
        {
            javalang.tree.LocalVariableDeclaration,
            javalang.tree.TryResource,
        }

    _ignore_node_types = \
        {
            javalang.tree.FormalParameter,
            javalang.tree.ReferenceType,
            javalang.tree.BasicType,
            javalang.tree.CatchClauseParameter,
            javalang.tree.Annotation,
            javalang.tree.TypeArgument,
        }

    _ignore_scope_statuses = \
        {
            ScopeStatusFlags.INSIDE_VARIABLE_DECLARATION_SUBTREE,
            ScopeStatusFlags.INSIDE_CALLING_SUPER_CLASS_CONSTRUCTOR_SUBTREE,
        }
