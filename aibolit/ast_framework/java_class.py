# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING, Dict, Set

from cached_property import cached_property  # type: ignore
from deprecated import deprecated  # type: ignore
from networkx import DiGraph  # type: ignore

from aibolit.ast_framework import AST, ASTNodeType, ASTNode
from aibolit.ast_framework.java_class_method import JavaClassMethod
from aibolit.ast_framework.java_class_field import JavaClassField

if TYPE_CHECKING:
    from aibolit.ast_framework.java_package import JavaPackage  # type: ignore


@deprecated(reason='This functionality must be transmitted to ASTNode')
class JavaClass(AST):
    def __init__(self, tree: DiGraph, root: int, java_package: 'JavaPackage'):
        super().__init__(tree, root)
        self._java_package = java_package

    def __str__(self):
        return f'Java class "{self.name}"'

    @cached_property
    def name(self) -> str:
        try:
            root_node = ASTNode(self.tree, self.root)
            class_name_nodes = [
                child for child in root_node.children if child.node_type == ASTNodeType.STRING
            ]
            if not class_name_nodes:
                msg = "Provided AST does not has 'STRING' node type right under the root"
                raise ValueError(msg)
            return class_name_nodes[0].string
        except ValueError:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def package(self) -> 'JavaPackage':
        return self._java_package

    @cached_property
    def methods(self) -> Dict[str, Set[JavaClassMethod]]:
        methods: Dict[str, Set[JavaClassMethod]] = {}
        for method_ast in self.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method = JavaClassMethod(method_ast.tree, method_ast.root, self)
            if method.name in methods:
                methods[method.name].add(method)
            else:
                methods[method.name] = {method}
        return methods

    @cached_property
    def fields(self) -> Dict[str, JavaClassField]:
        fields: Dict[str, JavaClassField] = {}
        for field_ast in self.get_subtrees(ASTNodeType.FIELD_DECLARATION):
            field = JavaClassField(field_ast.tree, field_ast.root, self)
            fields[field.name] = field
        return fields
