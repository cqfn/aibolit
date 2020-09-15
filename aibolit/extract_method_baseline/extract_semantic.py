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


from collections import OrderedDict
from typing import NamedTuple, Set, Dict

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class StatementSemantic(NamedTuple):
    used_variables: Set[str] = set()
    used_objects: Set[str] = set()
    used_methods: Set[str] = set()


def extract_method_statements_semantic(method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statement_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()
    for statement in method_ast.get_root().body:
        statement_semantic.update(extract_statement_semantic(statement, method_ast))

    return statement_semantic


def extract_statement_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    if statement.node_type == ASTNodeType.BLOCK_STATEMENT:
        return extract_block_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.FOR_STATEMENT:
        return extract_for_cycle_semantic(statement, method_ast)
    elif statement.node_type in {ASTNodeType.DO_STATEMENT, ASTNodeType.WHILE_STATEMENT}:
        return extract_while_cycle_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.IF_STATEMENT:
        return extract_if_branching_sematic(statement, method_ast)
    elif statement.node_type == ASTNodeType.SYNCHRONIZED_STATEMENT:
        return extract_synchronized_block_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.SWITCH_STATEMENT:
        return extract_switch_branching_semantic(statement, method_ast)
    elif statement.node_type == ASTNodeType.TRY_STATEMENT:
        return extract_try_block_semantic(statement, method_ast)
    elif statement.node_type in {
        ASTNodeType.ASSERT_STATEMENT,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.STATEMENT_EXPRESSION,
        ASTNodeType.THROW_STATEMENT,
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
    }:
        return extract_plain_statement_semantic(statement, method_ast)
    elif statement.node_type in {
        ASTNodeType.BREAK_STATEMENT,
        ASTNodeType.CONTINUE_STATEMENT,
    }:
        return OrderedDict()  # This statements are only single key word and has no semantic

    raise NotImplementedError(f"Extracting semantic from {statement.node_type} is not supported")


def extract_for_cycle_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    control_subtree = method_ast.get_subtree(statement.control)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, extract_semantic_from_ast(control_subtree))]
    )

    statements_semantic.update(extract_statement_semantic(statement.body, method_ast))

    return statements_semantic


def extract_block_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()
    for node in statement.statements:
        statements_semantic.update(extract_statement_semantic(node, method_ast))

    return statements_semantic


def extract_while_cycle_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    condition_subtree = method_ast.get_subtree(statement.condition)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, extract_semantic_from_ast(condition_subtree))]
    )

    statements_semantic.update(extract_statement_semantic(statement.body, method_ast))

    return statements_semantic


def extract_if_branching_sematic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    condition_subtree = method_ast.get_subtree(statement.condition)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, extract_semantic_from_ast(condition_subtree))]
    )

    statements_semantic.update(extract_statement_semantic(statement.then_statement, method_ast))

    if statement.else_statement is not None:
        statements_semantic.update(extract_statement_semantic(statement.else_statement, method_ast))

    return statements_semantic


def extract_synchronized_block_semantic(
    statement: ASTNode, method_ast: AST
) -> Dict[ASTNode, StatementSemantic]:
    lock_subtree = method_ast.get_subtree(statement.lock)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, extract_semantic_from_ast(lock_subtree))]
    )

    for inner_statement in statement.block:
        statements_semantic.update(extract_statement_semantic(inner_statement, method_ast))
    return statements_semantic


def extract_switch_branching_semantic(
    statement: ASTNode, method_ast: AST
) -> Dict[ASTNode, StatementSemantic]:
    expression_subtree = method_ast.get_subtree(statement.expression)
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict(
        [(statement, extract_semantic_from_ast(expression_subtree))]
    )

    for case in statement.cases:
        for inner_statement in case.statements:
            statements_semantic.update(extract_statement_semantic(inner_statement, method_ast))

    return statements_semantic


def extract_try_block_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statements_semantic: Dict[ASTNode, StatementSemantic] = OrderedDict()

    for resource in statement.resources or []:
        resource_ast = method_ast.get_subtree(resource)
        statements_semantic[resource] = extract_semantic_from_ast(resource_ast)

    for node in statement.block:
        statements_semantic.update(extract_statement_semantic(node, method_ast))

    for catch_clause in statement.catches or []:
        for inner_statement in catch_clause.block:
            statements_semantic.update(extract_statement_semantic(inner_statement, method_ast))

    for node in statement.finally_block or []:
        statements_semantic.update(extract_statement_semantic(node, method_ast))

    return statements_semantic


def extract_plain_statement_semantic(statement: ASTNode, method_ast: AST) -> Dict[ASTNode, StatementSemantic]:
    statement_ast = method_ast.get_subtree(statement)
    return OrderedDict([(statement, extract_semantic_from_ast(statement_ast))])


def extract_semantic_from_ast(statement_ast: AST) -> StatementSemantic:
    used_variables = set()
    used_objects = set()
    used_methods = set()

    for node in statement_ast.get_proxy_nodes(ASTNodeType.MEMBER_REFERENCE, ASTNodeType.METHOD_INVOCATION):
        if node.node_type == ASTNodeType.MEMBER_REFERENCE:
            used_variables.add(node.member)
        elif node.node_type == ASTNodeType.METHOD_INVOCATION:
            used_methods.add(node.member)

        if node.qualifier is not None:
            used_objects.add(node.qualifier)

    return StatementSemantic(
        used_methods=used_methods, used_objects=used_objects, used_variables=used_variables
    )
