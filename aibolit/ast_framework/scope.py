# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List, Iterator, Optional

from networkx import DiGraph  # type: ignore

from .ast import AST
from .ast_node import ASTNode
from .ast_node_type import ASTNodeType
from .scope_extractors import extract_scopes


class Scope:
    def __init__(self, scope_tree: DiGraph, scope_id: int):
        self._scope_tree = scope_tree
        self._scope_id = scope_id

    @staticmethod
    def build_from_method_ast(method_ast: AST) -> "Scope":
        method_declaration = method_ast.get_root()
        assert (
            method_declaration.node_type == ASTNodeType.METHOD_DECLARATION
        ), "Building scopes tree supported only for method declaration."

        scope_tree = DiGraph()
        root_scopes_id = Scope._create_scopes_from_node(method_declaration, method_ast, scope_tree)

        assert len(root_scopes_id) == 1, "Method declaration must produce a single scope."
        return Scope(scope_tree, root_scopes_id[0])

    @property
    def parent_scope(self) -> Optional["Scope"]:
        parent_scope_id: Optional[int] = next(self._scope_tree.predecessors(self._scope_id), None)

        if parent_scope_id is None:
            return None

        return Scope(self._scope_tree, parent_scope_id)

    @property
    def nested_scopes(self) -> Iterator["Scope"]:
        for nested_scope_id in self._scope_tree.successors(self._scope_id):
            yield Scope(self._scope_tree, nested_scope_id)

    @property
    def statements(self) -> List[ASTNode]:
        return self._scope_tree.nodes[self._scope_id]["statements"]

    @property
    def parent_node(self) -> ASTNode:
        return self._scope_tree.nodes[self._scope_id]["parent_node"]

    @property
    def parameters(self) -> List[ASTNode]:
        return self._scope_tree.nodes[self._scope_id]["parameters"]

    @staticmethod
    def _create_scopes_from_node(node: ASTNode, method_ast: AST, scope_tree: DiGraph) -> List[int]:
        scopes = extract_scopes(node, method_ast)

        new_scopes_ids: List[int] = []
        for scope in scopes:
            new_scope_id = len(scope_tree)
            new_scopes_ids.append(new_scope_id)
            scope_tree.add_node(
                new_scope_id,
                statements=scope.statements,
                parent_node=scope.parent_node,
                parameters=scope.parameters,
            )

            for statement in scope.statements:
                nested_scopes_ids = Scope._create_scopes_from_node(
                    statement, method_ast, scope_tree
                )
                for nested_scope_id in nested_scopes_ids:
                    scope_tree.add_edge(new_scope_id, nested_scope_id)

        return new_scopes_ids
