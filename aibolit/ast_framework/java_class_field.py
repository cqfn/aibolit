# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING

from cached_property import cached_property  # type: ignore
from deprecated import deprecated  # type: ignore
from networkx import DiGraph  # type: ignore

from aibolit.ast_framework import AST, ASTNodeType

if TYPE_CHECKING:
    from aibolit.ast_framework.java_class import JavaClass


@deprecated("This functionality must be transmitted to ASTNode")
class JavaClassField(AST):
    def __init__(self, tree: DiGraph, root: int, java_class: 'JavaClass'):
        super().__init__(tree, root)
        self._java_class = java_class

    @cached_property
    def name(self) -> str:
        try:
            field_declarator = next(
                self.children_with_type(self.root, ASTNodeType.VARIABLE_DECLARATOR)
            )
            field_name = next(self.children_with_type(field_declarator, ASTNodeType.STRING))
            return self.tree.nodes[field_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def java_class(self) -> 'JavaClass':
        return self._java_class
