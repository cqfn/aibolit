# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import TYPE_CHECKING, Dict

from cached_property import cached_property  # type: ignore
from deprecated import deprecated  # type: ignore
from networkx import DiGraph  # type: ignore

from aibolit.ast_framework import AST, ASTNodeType, ASTNode
from aibolit.utils.cfg_builder import build_cfg

if TYPE_CHECKING:
    from aibolit.ast_framework.java_class import JavaClass  # type: ignore


@deprecated(reason='This functionality must be transmitted to ASTNode')
class JavaClassMethod(AST):
    def __init__(self, tree: DiGraph, root: int, java_class: 'JavaClass'):
        super().__init__(tree, root)
        self._java_class = java_class

    def __str__(self):
        return f'Method {self.name}'

    @cached_property
    def name(self) -> str:
        try:
            root_node = ASTNode(self.tree, self.root)
            method_name_nodes = [
                child for child in root_node.children if child.node_type == ASTNodeType.STRING
            ]
            if not method_name_nodes:
                msg = "Provided AST does not has 'STRING' node type right under the root"
                raise ValueError(msg)
            return method_name_nodes[0].string
        except ValueError:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def java_class(self) -> 'JavaClass':
        return self._java_class

    @cached_property
    def parameters(self) -> Dict[str, AST]:
        parameters: Dict[str, AST] = {}
        for parameter in self.get_subtrees(ASTNodeType.FORMAL_PARAMETER):
            parameter_node = ASTNode(self.tree, parameter.root)
            string_children = [
                child for child in parameter_node.children
                if child.node_type == ASTNodeType.STRING
            ]
            if string_children:
                parameter_name = string_children[0].string
                parameters[parameter_name] = parameter
        return parameters

    @cached_property
    def body(self) -> AST:
        return self.get_subtree(self.get_root())

    @cached_property
    def cfg(self) -> DiGraph:
        return build_cfg(self.body)
