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
    _scoped_node_types = {
        ASTNodeType.BLOCK_STATEMENT,
        ASTNodeType.FOR_STATEMENT,
    }
    _declaration_node_types = {
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ASTNodeType.VARIABLE_DECLARATION,
    }

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
        self._walk_nodes(method.body, states, scopes)
        return self._collect_bidirect_lines(states)

    def _walk_nodes(
        self,
        node_or_nodes: Any,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
    ) -> None:
        if isinstance(node_or_nodes, list):
            for node in node_or_nodes:
                self._walk_nodes(node, states, scopes)
            return

        node = node_or_nodes
        creates_scope = node.node_type in self._scoped_node_types
        if creates_scope:
            scopes.append({})
        try:
            self._process_node(node, states, scopes)
            for child in node.children:
                self._walk_nodes(child, states, scopes)
        finally:
            if creates_scope:
                scopes.pop()

    def _process_node(
        self,
        node: ASTNode,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
    ) -> None:
        if node.node_type in self._declaration_node_types:
            self._declare(node, states, scopes)
        elif node.node_type == ASTNodeType.MEMBER_REFERENCE:
            self._mark_unary(node, states, scopes)
        elif node.node_type == ASTNodeType.ASSIGNMENT:
            self._mark_assignment(node, states, scopes)

    def _declare(
        self,
        node: ASTNode,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
    ) -> None:
        for name in node.names:
            state = _VariableState(node.line)
            scopes[-1][name] = state
            states.append(state)

    def _lookup(
        self,
        scopes: list[dict[str, _VariableState]],
        name: str,
    ) -> _VariableState | None:
        for scope in reversed(scopes):
            if name in scope:
                return scope[name]
        return None

    def _candidate(
        self,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
        name: str,
        line: int,
    ) -> _VariableState:
        state = self._lookup(scopes, name)
        if state is None:
            state = _VariableState(line)
            scopes[-1][name] = state
            states.append(state)
        return state

    def _mark_unary(
        self,
        node: ASTNode,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
    ) -> None:
        name = self._member_name(node)
        if name is None:
            return
        operators = set(node.prefix_operators + node.postfix_operators)
        state = self._candidate(states, scopes, name, node.line)
        if '++' in operators:
            state.increments += 1
        if '--' in operators:
            state.decrements += 1

    def _mark_assignment(
        self,
        node: ASTNode,
        states: list[_VariableState],
        scopes: list[dict[str, _VariableState]],
    ) -> None:
        name = self._member_name(node.expressionl)
        if name is None:
            return
        state = self._candidate(states, scopes, name, node.line)
        if node.type == '+=':
            state.increments += 1
            return
        if node.type == '-=':
            state.decrements += 1
            return
        if node.type == '=':
            self._mark_self_update(state, name, node.value)

    @staticmethod
    def _member_name(node: ASTNode) -> str | None:
        if node.node_type == ASTNodeType.MEMBER_REFERENCE and node.qualifier is None:
            return node.member
        return None

    def _mark_self_update(self, state: _VariableState, name: str, value: ASTNode) -> None:
        if value.node_type != ASTNodeType.BINARY_OPERATION:
            return
        if value.operator == '+' and self._is_same_variable(name, value):
            state.increments += 1
        elif value.operator == '-' and self._member_name(value.operandl) == name:
            state.decrements += 1

    def _is_same_variable(self, name: str, value: ASTNode) -> bool:
        return (
            self._member_name(value.operandl) == name or
            self._member_name(value.operandr) == name
        )

    @staticmethod
    def _collect_bidirect_lines(states: list[_VariableState]) -> list[int]:
        return [
            state.line
            for state in states
            if state.increments > 0 and state.decrements > 0
        ]
