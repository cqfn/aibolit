# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import dataclasses
import os
from typing import Callable, Dict, Iterable, List, Optional, Set

from aibolit.ast_framework.ast import AST
from aibolit.ast_framework.ast_node import ASTNode
from aibolit.ast_framework.ast_node_type import ASTNodeType
from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast

_INCREMENT = 'increment'
_DECREMENT = 'decrement'


@dataclasses.dataclass
class _VarState:
    """Tracks how a single variable is mutated inside one scope."""

    declaration_line: Optional[int] = None
    directions: Set[str] = dataclasses.field(default_factory=set)
    first_line: Optional[int] = None

    def record(self, direction: Optional[str], line: int) -> None:
        if direction is not None:
            self.directions.add(direction)
        if self.first_line is None or line < self.first_line:
            self.first_line = line

    def is_bidirectional(self) -> bool:
        return _INCREMENT in self.directions and _DECREMENT in self.directions

    def report_line(self) -> int:
        # Report the declaration when the variable is declared, otherwise the
        # first line where it is used (e.g. a field assigned inside the method).
        line = self.declaration_line if self.declaration_line is not None else self.first_line
        assert line is not None  # set whenever a direction was recorded
        return line


@dataclasses.dataclass
class _Scope:
    variables: Dict[str, _VarState] = dataclasses.field(default_factory=dict)


class BidirectIndex:
    """
    Finds numeric variables that are both incremented and decremented within the
    same method. A counter/index should consistently grow or shrink; mixing both
    directions makes the index confusing to follow.
    """

    _scope_node_types = frozenset({
        ASTNodeType.METHOD_DECLARATION,
        ASTNodeType.CONSTRUCTOR_DECLARATION,
        ASTNodeType.LAMBDA_EXPRESSION,
        ASTNodeType.FOR_STATEMENT,
        ASTNodeType.WHILE_STATEMENT,
        ASTNodeType.DO_STATEMENT,
        ASTNodeType.BLOCK_STATEMENT,
        ASTNodeType.TRY_STATEMENT,
        ASTNodeType.SWITCH_STATEMENT,
        ASTNodeType.CATCH_CLAUSE,
    })

    def __init__(self):
        pass

    def value(self, filename: str | os.PathLike) -> List[LineNumber]:
        """
        Finds if a variable is being incremented and decremented within the same method

        :param filename: filename to be analyzed
        :return: list of LineNumber with the variable declaration lines
        """
        ast = AST.build_from_javalang(build_ast(filename))
        result: Set[LineNumber] = set()
        for method in ast.proxy_nodes(
            ASTNodeType.METHOD_DECLARATION, ASTNodeType.CONSTRUCTOR_DECLARATION
        ):
            result.update(self._analyze_method(ast.subtree(method)))
        return sorted(result)

    def _analyze_method(self, method_ast: AST) -> Set[LineNumber]:
        scopes: List[_Scope] = []
        free: Dict[str, _VarState] = {}
        flagged: Set[LineNumber] = set()

        def resolve(name: str) -> _VarState:
            for scope in reversed(scopes):
                if name in scope.variables:
                    return scope.variables[name]
            return free.setdefault(name, _VarState())

        def on_enter(node: ASTNode) -> None:
            if node.node_type in self._scope_node_types:
                scopes.append(_Scope())
            elif node.node_type == ASTNodeType.VARIABLE_DECLARATOR:
                scopes[-1].variables[node.name] = _VarState(declaration_line=node.line)
            else:
                self._register_operation(node, resolve)

        def on_leave(node: ASTNode) -> None:
            if node.node_type in self._scope_node_types:
                self._collect(scopes.pop().variables.values(), flagged)

        method_ast.traverse(on_enter, on_leave)
        self._collect(free.values(), flagged)
        return flagged

    @staticmethod
    def _collect(states: Iterable[_VarState], flagged: Set[LineNumber]) -> None:
        for state in states:
            if state.is_bidirectional():
                flagged.add(state.report_line())

    def _register_operation(
        self, node: ASTNode, resolve: Callable[[str], _VarState]
    ) -> None:
        if node.node_type == ASTNodeType.MEMBER_REFERENCE:
            operators = set(node.prefix_operators) | set(node.postfix_operators)
            if '++' in operators:
                resolve(node.member).record(_INCREMENT, node.line)
            elif '--' in operators:
                resolve(node.member).record(_DECREMENT, node.line)
        elif node.node_type == ASTNodeType.ASSIGNMENT:
            target = node.expressionl
            if target.node_type == ASTNodeType.MEMBER_REFERENCE:
                resolve(target.member).record(
                    self._assignment_direction(node, target.member), node.line
                )

    def _assignment_direction(self, node: ASTNode, name: str) -> Optional[str]:
        if node.type == '+=':
            return _INCREMENT
        if node.type == '-=':
            return _DECREMENT
        value = node.value
        if node.type == '=' and value is not None and \
                value.node_type == ASTNodeType.BINARY_OPERATION:
            if value.operator == '+' and (
                self._is_member(value.operandl, name) or self._is_member(value.operandr, name)
            ):
                return _INCREMENT
            if value.operator == '-' and self._is_member(value.operandl, name):
                return _DECREMENT
        return None

    @staticmethod
    def _is_member(node: Optional[ASTNode], name: str) -> bool:
        return node is not None and \
            node.node_type == ASTNodeType.MEMBER_REFERENCE and node.member == name
