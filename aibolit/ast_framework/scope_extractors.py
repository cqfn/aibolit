# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import Dict, List, Callable, NamedTuple
from itertools import chain

from .ast import AST
from .ast_node import ASTNode
from .ast_node_type import ASTNodeType


class ScopeAttributes(NamedTuple):
    statements: List[ASTNode]
    parent_node: ASTNode
    parameters: List[ASTNode] = []


def extract_scopes(node: ASTNode, ast: AST) -> List[ScopeAttributes]:
    try:
        return _scope_extractors_by_node_type[node.node_type](node, ast)
    except KeyError:
        return []


def _extract_scopes_from_assert(assert_node: ASTNode, method_ast: AST) -> List[ScopeAttributes]:
    assert assert_node.node_type == ASTNodeType.ASSERT_STATEMENT

    expression_ast = method_ast.get_subtree(assert_node.condition)
    return _find_scopes_in_expressions(expression_ast)


def _extract_scopes_from_block(block_node: ASTNode, _) -> List[ScopeAttributes]:
    assert block_node.node_type == ASTNodeType.BLOCK_STATEMENT

    return [ScopeAttributes(statements=block_node.statements, parent_node=block_node)]


def _extract_scopes_from_expression_statement(
    expression_statement: ASTNode, method_ast: AST
) -> List[ScopeAttributes]:
    assert expression_statement.node_type in {
        ASTNodeType.STATEMENT_EXPRESSION,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.THROW_STATEMENT,
    }

    expression_ast = method_ast.get_subtree(expression_statement.expression)
    return _find_scopes_in_expressions(expression_ast)


def _extract_scopes_from_for_cycle(for_cycle: ASTNode, method_ast: AST) -> List[ScopeAttributes]:
    assert for_cycle.node_type == ASTNodeType.FOR_STATEMENT

    control_ast = method_ast.get_subtree(for_cycle.control)
    scopes = _find_scopes_in_expressions(control_ast)
    scopes.append(
        ScopeAttributes(
            statements=_get_block_statements_list(for_cycle.body), parent_node=for_cycle
        )
    )

    return scopes


def _extract_scopes_from_if_statement(if_node: ASTNode, method_ast: AST) -> List[ScopeAttributes]:
    assert if_node.node_type == ASTNodeType.IF_STATEMENT

    condition_ast = method_ast.get_subtree(if_node.condition)
    scopes = _find_scopes_in_expressions(condition_ast)
    scopes.append(
        ScopeAttributes(
            statements=_get_block_statements_list(if_node.then_statement), parent_node=if_node
        )
    )

    while (
        if_node.else_statement is not None and
        if_node.else_statement.node_type == ASTNodeType.IF_STATEMENT
    ):
        if_node = if_node.else_statement
        condition_ast = method_ast.get_subtree(if_node.condition)
        scopes.extend(_find_scopes_in_expressions(condition_ast))
        scopes.append(
            ScopeAttributes(
                statements=_get_block_statements_list(if_node.then_statement), parent_node=if_node
            )
        )

    if if_node.else_statement is not None:
        scopes.append(
            ScopeAttributes(
                statements=_get_block_statements_list(if_node.else_statement), parent_node=if_node
            )
        )

    return scopes


def _extract_scopes_from_variable_declaration(
    variable_declaration: ASTNode, method_ast: AST
) -> List[ScopeAttributes]:
    assert variable_declaration.node_type == ASTNodeType.LOCAL_VARIABLE_DECLARATION

    return list(
        chain.from_iterable(
            _find_scopes_in_expressions(method_ast.get_subtree(declarator.initializer))
            for declarator in variable_declaration.declarators
        )
    )


def _extract_scopes_from_method(method_declaration: ASTNode, _) -> List[ScopeAttributes]:
    assert method_declaration.node_type == ASTNodeType.METHOD_DECLARATION

    return [ScopeAttributes(statements=method_declaration.body, parent_node=method_declaration)]


def _extract_scopes_from_switch_statement(
    switch_statement: ASTNode, method_ast: AST
) -> List[ScopeAttributes]:
    assert switch_statement.node_type == ASTNodeType.SWITCH_STATEMENT

    expression_ast = method_ast.get_subtree(switch_statement.expression)
    scopes = _find_scopes_in_expressions(expression_ast)

    # all case statements belong to one scope
    # thats why cases are not surrounded with curly braces
    scopes.append(
        ScopeAttributes(
            statements=list(
                chain.from_iterable(case_node.statements for case_node in switch_statement.cases)
            ),
            parent_node=switch_statement,
        )
    )

    return scopes


def _extract_scopes_from_synchronized(
    synchronized_block: ASTNode, method_ast: AST
) -> List[ScopeAttributes]:
    assert synchronized_block.node_type == ASTNodeType.SYNCHRONIZED_STATEMENT

    lock_ast = method_ast.get_subtree(synchronized_block.lock)
    scopes = _find_scopes_in_expressions(lock_ast)
    scopes.append(
        ScopeAttributes(statements=synchronized_block.block, parent_node=synchronized_block)
    )

    return scopes


def _extract_scopes_from_try_statement(try_node: ASTNode, method_ast: AST) -> List[ScopeAttributes]:
    assert try_node.node_type == ASTNodeType.TRY_STATEMENT

    scopes: List[ScopeAttributes] = []

    for resource in try_node.resources:
        initializer_ast = method_ast.get_subtree(resource.value)
        scopes.extend(_find_scopes_in_expressions(initializer_ast))

    scopes.append(ScopeAttributes(statements=try_node.block, parent_node=try_node))

    for catch in try_node.catches:
        scopes.append(
            ScopeAttributes(statements=catch.block, parent_node=try_node)
        )

    if try_node.finally_block is not None:
        scopes.append(
            ScopeAttributes(statements=try_node.finally_block, parent_node=try_node)
        )

    return scopes


def _extract_scopes_from_while_cycle(
    while_cycle: ASTNode, method_ast: AST
) -> List[ScopeAttributes]:
    assert while_cycle.node_type in {ASTNodeType.DO_STATEMENT, ASTNodeType.WHILE_STATEMENT}

    condition_ast = method_ast.get_subtree(while_cycle.condition)
    scopes = _find_scopes_in_expressions(condition_ast)
    scopes.append(
        ScopeAttributes(
            statements=_get_block_statements_list(while_cycle.body), parent_node=while_cycle
        )
    )

    return scopes


def _find_scopes_in_expressions(expression_ast: AST) -> List[ScopeAttributes]:
    """
    Finds top level lambda expressions and returns their bodies.
    Each found nested scope represented by a list of its statements. List of such list is returned.
    TO-FIX: Add support for others scopes can be found in expressions like anonymous classes.
    """

    nested_scopes_statements: List[ScopeAttributes] = []
    for nested_scope in expression_ast.get_subtrees(ASTNodeType.LAMBDA_EXPRESSION):
        lambda_declaration = nested_scope.get_root()
        nested_scopes_statements.append(
            ScopeAttributes(
                statements=lambda_declaration.body,
                parent_node=lambda_declaration,
                parameters=lambda_declaration.parameters,
            )
        )

    return nested_scopes_statements


def _get_block_statements_list(node: ASTNode) -> List[ASTNode]:
    if node.node_type == ASTNodeType.BLOCK_STATEMENT:
        return node.statements

    # there may be a single statement without curly braces
    # for consistency we wrap it in a list
    return [node]


_scope_extractors_by_node_type: Dict[
    ASTNodeType, Callable[[ASTNode, AST], List[ScopeAttributes]]
] = {
    ASTNodeType.ASSERT_STATEMENT: _extract_scopes_from_assert,
    ASTNodeType.BLOCK_STATEMENT: _extract_scopes_from_block,
    ASTNodeType.DO_STATEMENT: _extract_scopes_from_while_cycle,
    ASTNodeType.FOR_STATEMENT: _extract_scopes_from_for_cycle,
    ASTNodeType.IF_STATEMENT: _extract_scopes_from_if_statement,
    ASTNodeType.LOCAL_VARIABLE_DECLARATION: _extract_scopes_from_variable_declaration,
    ASTNodeType.METHOD_DECLARATION: _extract_scopes_from_method,
    ASTNodeType.RETURN_STATEMENT: _extract_scopes_from_expression_statement,
    ASTNodeType.STATEMENT_EXPRESSION: _extract_scopes_from_expression_statement,
    ASTNodeType.SWITCH_STATEMENT: _extract_scopes_from_switch_statement,
    ASTNodeType.SYNCHRONIZED_STATEMENT: _extract_scopes_from_synchronized,
    ASTNodeType.THROW_STATEMENT: _extract_scopes_from_expression_statement,
    ASTNodeType.TRY_STATEMENT: _extract_scopes_from_try_statement,
    ASTNodeType.WHILE_STATEMENT: _extract_scopes_from_while_cycle,
}
