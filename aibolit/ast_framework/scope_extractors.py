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

from typing import Dict, List, Callable
from itertools import chain

from .ast import AST
from .ast_node import ASTNode
from .ast_node_type import ASTNodeType

Statements = List[ASTNode]


def _extract_scope_statements_from_assert(assert_node: ASTNode, method_ast: AST) -> List[Statements]:
    assert assert_node.node_type == ASTNodeType.ASSERT_STATEMENT

    expression_ast = method_ast.get_subtree(assert_node.condition)
    return _find_nested_scopes_in_expressions(expression_ast)


def _extract_scope_statements_from_expression_statement(
    expression_statement: ASTNode, method_ast: AST
) -> List[Statements]:
    assert expression_statement.node_type in {
        ASTNodeType.STATEMENT_EXPRESSION,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.THROW_STATEMENT,
    }

    expression_ast = method_ast.get_subtree(expression_statement.expression)
    return _find_nested_scopes_in_expressions(expression_ast)


def _extract_scope_statements_from_for_cycle(for_cycle: ASTNode, method_ast: AST) -> List[Statements]:
    assert for_cycle.node_type == ASTNodeType.FOR_STATEMENT

    control_ast = method_ast.get_subtree(for_cycle.control)
    scope_statements = _find_nested_scopes_in_expressions(control_ast)
    scope_statements.append(_get_block_statements_list(for_cycle.body))

    return scope_statements


def _extract_scope_statements_from_if_statement(if_node: ASTNode, method_ast: AST) -> List[Statements]:
    assert if_node.node_type == ASTNodeType.IF_STATEMENT

    condition_ast = method_ast.get_subtree(if_node.condition)
    scope_statements = _find_nested_scopes_in_expressions(condition_ast)
    scope_statements.append(_get_block_statements_list(if_node.then_statement))

    while if_node.else_statement is not None and if_node.else_statement.node_type == ASTNodeType.IF_STATEMENT:
        if_node = if_node.else_statement
        condition_ast = method_ast.get_subtree(if_node.condition)
        scope_statements.extend(_find_nested_scopes_in_expressions(condition_ast))
        scope_statements.append(_get_block_statements_list(if_node.then_statement))

    if if_node.else_statement is not None:
        scope_statements.append(_get_block_statements_list(if_node.else_statement))

    return scope_statements


def _extract_scope_statements_from_variable_declaration(
    variable_declaration: ASTNode, method_ast: AST
) -> List[Statements]:
    assert variable_declaration.node_type == ASTNodeType.LOCAL_VARIABLE_DECLARATION

    return list(
        chain.from_iterable(
            _find_nested_scopes_in_expressions(method_ast.get_subtree(declarator.initializer))
            for declarator in variable_declaration.declarators
        )
    )


def _extract_scope_statements_from_switch_statement(
    switch_statement: ASTNode, method_ast: AST
) -> List[Statements]:
    assert switch_statement.node_type == ASTNodeType.SWITCH_STATEMENT

    expression_ast = method_ast.get_subtree(switch_statement.expression)
    scope_statements = _find_nested_scopes_in_expressions(expression_ast)

    # all case statements belong to one scope
    # thats why cases are not surrounded with curly braces
    scope_statements.append(
        list(chain.from_iterable(case_node.statements for case_node in switch_statement.cases))
    )

    return scope_statements


def _extract_scope_statements_from_synchronized(
    synchronized_block: ASTNode, method_ast: AST
) -> List[Statements]:
    assert synchronized_block.node_type == ASTNodeType.SYNCHRONIZED_STATEMENT

    lock_ast = method_ast.get_subtree(synchronized_block.lock)
    scope_statements = _find_nested_scopes_in_expressions(lock_ast)
    scope_statements.append(synchronized_block.block)

    return scope_statements


def _extract_scope_statements_from_try_statement(try_node: ASTNode, method_ast: AST) -> List[Statements]:
    assert try_node.node_type == ASTNodeType.TRY_STATEMENT

    scope_statements: List[Statements] = []

    for resource in try_node.resources:
        initializer_ast = method_ast.get_subtree(resource.value)
        scope_statements.extend(_find_nested_scopes_in_expressions(initializer_ast))

    scope_statements.append(try_node.block)

    for catch in try_node.catches:
        scope_statements.append(catch.block)

    if try_node.finally_block is not None:
        scope_statements.append(try_node.finally_block)

    return scope_statements


def _extract_scope_statements_from_while_cycle(while_cycle: ASTNode, method_ast: AST) -> List[Statements]:
    assert while_cycle.node_type in {ASTNodeType.DO_STATEMENT, ASTNodeType.WHILE_STATEMENT}

    condition_ast = method_ast.get_subtree(while_cycle.condition)
    scope_statements = _find_nested_scopes_in_expressions(condition_ast)
    scope_statements.append(_get_block_statements_list(while_cycle.body))

    return scope_statements


def _find_nested_scopes_in_expressions(expression_ast: AST) -> List[Statements]:
    """
    Finds top level lambda expressions and returns their bodies.
    Each found nested scope represented by a list of its statements. List of such list is returned.
    TODO: Add support for others scopes can be found in expressions like anonymous classes.
    """

    nested_scopes_statements: List[Statements] = []
    for nested_scope in expression_ast.get_subtrees(ASTNodeType.LAMBDA_EXPRESSION):
        nested_scopes_statements.append(nested_scope.get_root().body)

    return nested_scopes_statements


def _get_block_statements_list(node: ASTNode) -> List[ASTNode]:
    if node.node_type == ASTNodeType.BLOCK_STATEMENT:
        return node.statements

    # there may be a single statement without curly braces
    # for consistency we wrap it in a list
    return [node]


scope_extractors_by_node_type: Dict[ASTNodeType, Callable[[ASTNode, AST], List[Statements]]] = {
    ASTNodeType.ASSERT_STATEMENT: _extract_scope_statements_from_assert,
    ASTNodeType.BLOCK_STATEMENT: lambda node, _: [node.statements],
    ASTNodeType.DO_STATEMENT: _extract_scope_statements_from_while_cycle,
    ASTNodeType.FOR_STATEMENT: _extract_scope_statements_from_for_cycle,
    ASTNodeType.IF_STATEMENT: _extract_scope_statements_from_if_statement,
    ASTNodeType.LOCAL_VARIABLE_DECLARATION: _extract_scope_statements_from_variable_declaration,
    ASTNodeType.METHOD_DECLARATION: lambda node, _: [node.body],
    ASTNodeType.RETURN_STATEMENT: _extract_scope_statements_from_expression_statement,
    ASTNodeType.STATEMENT_EXPRESSION: _extract_scope_statements_from_expression_statement,
    ASTNodeType.SWITCH_STATEMENT: _extract_scope_statements_from_switch_statement,
    ASTNodeType.SYNCHRONIZED_STATEMENT: _extract_scope_statements_from_synchronized,
    ASTNodeType.THROW_STATEMENT: _extract_scope_statements_from_expression_statement,
    ASTNodeType.TRY_STATEMENT: _extract_scope_statements_from_try_statement,
    ASTNodeType.WHILE_STATEMENT: _extract_scope_statements_from_while_cycle,
}
