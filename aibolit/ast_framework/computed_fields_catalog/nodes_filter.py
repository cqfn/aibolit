# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import Callable, Iterator

from aibolit.ast_framework import ASTNode, ASTNodeType


def nodes_filter_factory(
    base_field_name: str, *node_types: ASTNodeType
) -> Callable[[ASTNode], Iterator[ASTNode]]:
    """
    Create filter, which takes 'body_field_name' field of incoming node,
    checks if it list of ASTNode, and return it filtered by node_type.
    """

    def filter(base_node: ASTNode) -> Iterator[ASTNode]:
        base_field = getattr(base_node, base_field_name)
        if isinstance(base_field, list):
            for node in base_field:
                if isinstance(node, ASTNode) and node.node_type in node_types:
                    yield node
        else:
            raise RuntimeError(
                f"Failed computing ASTNode field based on {base_field_name} field. "
                f"Expected list, but got {base_field} of type {type(base_field)}."
            )

    return filter
