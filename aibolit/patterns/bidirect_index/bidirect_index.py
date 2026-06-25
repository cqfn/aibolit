# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os
from dataclasses import dataclass
from typing import Any

from aibolit.ast_framework import AST, ASTNode, ASTNodeType
from aibolit.utils.ast_builder import build_ast


@dataclass
class _VariableState:
    line: int
    increments: int = 0
    decrements: int = 0


class BidirectIndex:

    def value(self, filename: str | os.PathLike | AST):
        """
        Finds if a variable is being incremented and decremented within the same method

        :param filename: filename or AST to be analyzed
        :return: list of LineNumber with the variable declaration lines
        """
        ast = self._ast(filename)
        lines: list[int] = []
        for method in ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            lines.extend(self._bidirect_lines_in_method(method))
        return sorted(lines)

    def _ast(self, source: str | os.PathLike | AST) -> AST:
        if isinstance(source, AST):
            return source
        return AST.build_from_javalang(build_ast(source))

    def _bidirect_lines_in_method(self, method: ASTNode) -> list[int]:
        states: list[_VariableState] = []
        scopes: list[dict[str, _VariableState]] = [{}]

        def lookup(name: str) -> _VariableState | None:
            for scope in reversed(scopes):
                if name in scope:
                    return scope[name]
            return None

        def candidate(name: str, line: int) -> _VariableState:
            state = lookup(name)
            if state is None:
                state = _VariableState(line)
                scopes[-1][name] = state
                states.append(state)
            return state

        def declare(node: ASTNode) -> None:
            for name in node.names:
                state = _VariableState(node.line)
                scopes[-1][name] = state
                states.append(state)

        def member_name(node: ASTNode) -> str | None:
            if node.node_type == ASTNodeType.MEMBER_REFERENCE and node.qualifier is None:
                return node.member
            return None

        def mark_unary(node: ASTNode) -> None:
            name = member_name(node)
            if name is None:
                return
            operators = set(node.prefix_operators + node.postfix_operators)
            state = candidate(name, node.line)
            if '++' in operators:
                state.increments += 1
            if '--' in operators:
                state.decrements += 1

        def mark_assignment(node: ASTNode) -> None:
            name = member_name(node.expressionl)
            if name is None:
                return
            state = candidate(name, node.line)
            if node.type == '+=':
                state.increments += 1
            elif node.type == '-=':
                state.decrements += 1
            elif node.type == '=':
                mark_self_update(state, name, node.value)

        def mark_self_update(state: _VariableState, name: str, value: ASTNode) -> None:
            if value.node_type != ASTNodeType.BINARY_OPERATION:
                return
            if value.operator == '+' and (
                member_name(value.operandl) == name or member_name(value.operandr) == name
            ):
                state.increments += 1
            elif value.operator == '-' and member_name(value.operandl) == name:
                state.decrements += 1

        def walk(node_or_nodes: Any) -> None:
            if isinstance(node_or_nodes, list):
                for node in node_or_nodes:
                    walk(node)
                return

            node = node_or_nodes
            creates_scope = node.node_type in {
                ASTNodeType.BLOCK_STATEMENT,
                ASTNodeType.FOR_STATEMENT,
            }
            if creates_scope:
                scopes.append({})
            try:
                if node.node_type in {
                    ASTNodeType.LOCAL_VARIABLE_DECLARATION,
                    ASTNodeType.VARIABLE_DECLARATION,
                }:
                    declare(node)
                elif node.node_type == ASTNodeType.MEMBER_REFERENCE:
                    mark_unary(node)
                elif node.node_type == ASTNodeType.ASSIGNMENT:
                    mark_assignment(node)

                for child in node.children:
                    walk(child)
            finally:
                if creates_scope:
                    scopes.pop()

        walk(method.body)
        return [
            state.line
            for state in states
            if state.increments > 0 and state.decrements > 0
        ]
