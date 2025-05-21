# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from collections import defaultdict
import sys
from typing import Dict, Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from aibolit.ast_framework import ASTNode, ASTNodeType  # noqa: F401


class _ComputedFieldsRegistry:
    def __init__(self) -> None:
        RegistryType = Dict["ASTNodeType", Dict[str, Callable[["ASTNode"], Any]]]
        self._registry: RegistryType = defaultdict(dict)

    def register(
        self,
        compute_field: Callable[["ASTNode"], Any],
        name: str,
        *node_types: "ASTNodeType",
    ) -> None:
        for node_type in node_types:
            computed_fields = self._registry[node_type]
            if name in computed_fields and \
               not _ComputedFieldsRegistry._is_in_interactive_shell():
                raise RuntimeError(
                    f"Registry already has computed field "
                    f"named '{name}' for node type {node_type}."
                )

            computed_fields[name] = compute_field

    def get_fields(
        self, node_type: "ASTNodeType"
    ) -> Dict[str, Callable[["ASTNode"], Any]]:
        return self._registry[node_type]

    def clear(self) -> None:
        self._registry = defaultdict(dict)

    @staticmethod
    def _is_in_interactive_shell() -> bool:
        """
        Taken from comments to this answer https://stackoverflow.com/a/6879085/2129920
        """
        return bool(getattr(sys, "ps1", sys.flags.interactive))


computed_fields_registry = _ComputedFieldsRegistry()
