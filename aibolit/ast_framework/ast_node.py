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

from typing import Any, List, Iterator, Optional

from networkx import DiGraph, dfs_preorder_nodes  # type: ignore
from cached_property import cached_property  # type: ignore

from aibolit.ast_framework._auxiliary_data import (
    common_attributes,
    attributes_by_node_type,
    ASTNodeReference,
)
from aibolit.ast_framework import ASTNodeType
from aibolit.ast_framework.computed_fields_registry import computed_fields_registry


class ASTNode:
    def __init__(self, graph: DiGraph, node_index: int):
        self._graph = graph
        self._node_index = node_index

    @property
    def children(self) -> Iterator["ASTNode"]:
        for child_index in self._graph.succ[self._node_index]:
            yield ASTNode(self._graph, child_index)

    @property
    def node_index(self) -> int:
        return self._node_index

    @cached_property
    def line(self) -> int:
        line = self._get_line(self._node_index)
        if line is not None:
            return line

        children_lines: List[int] = [
            self._get_line(child_index)  # type: ignore # all Nones filtered out in list comprehension
            for child_index in dfs_preorder_nodes(self._graph, self._node_index)
            if self._get_line(child_index) is not None
        ]

        # try to find source code line information from nodes reachable from self
        if children_lines:
            return min(children_lines)

        # try to  find source code line information from parents up to the root
        parent_index = self._get_parent(self._node_index)
        while line is None and parent_index is not None:
            line = self._get_line(parent_index)
            parent_index = self._get_parent(parent_index)

        if line is not None:
            return line

        raise RuntimeError(
            f"Failed to retrieve source code line information for {repr(self)} node. "
            "All nodes in a path from root to it and all nodes, reachable from it, "
            "does not have any source code line information either."
        )

    def __getattr__(self, attribute_name: str):
        node_type = self._get_type(self._node_index)
        existing_fields_names = attributes_by_node_type[node_type]
        computed_fields = computed_fields_registry.get_fields(node_type)
        if attribute_name not in common_attributes and \
           attribute_name not in existing_fields_names and \
           attribute_name not in computed_fields:
            raise AttributeError(
                "Failed to retrieve property. "
                f"'{node_type}' node does not have '{attribute_name}' attribute."
            )

        if attribute_name in computed_fields:
            attribute = computed_fields[attribute_name](self)
        else:
            attribute = self._graph.nodes[self._node_index][attribute_name]

        if isinstance(attribute, ASTNodeReference):
            attribute = self._create_node_from_reference(attribute)
        elif isinstance(attribute, list):
            attribute = self._replace_references_with_nodes(attribute)
        return attribute

    def __dir__(self) -> List[str]:
        node_type = self._get_type(self._node_index)
        return ASTNode._public_fixed_interface + \
            list(common_attributes) + \
            list(attributes_by_node_type[node_type]) + \
            list(computed_fields_registry.get_fields(node_type).keys())

    def __str__(self) -> str:
        text_representation = f"node index: {self._node_index}"
        node_type = self._get_type(self._node_index)
        for attribute_name in sorted(
            common_attributes | attributes_by_node_type[node_type]
        ):
            attribute_value = self.__getattr__(attribute_name)

            if isinstance(attribute_value, ASTNode):
                attribute_representation = repr(attribute_value)
            elif isinstance(attribute_value, str) and "\n" in attribute_value:
                attribute_representation = "\n\t" + attribute_value.replace(
                    "\n", "\n\t"
                )
            else:
                attribute_representation = str(attribute_value)

            text_representation += f"\n{attribute_name}: {attribute_representation}"

        return text_representation

    def __repr__(self) -> str:
        return f"<ASTNode node_type: {self._get_type(self._node_index)}, node_index: {self._node_index}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ASTNode):
            raise NotImplementedError(
                f"ASTNode support comparission only with themselves, but {type(other)} was provided."
            )
        return self._graph == other._graph and self._node_index == other._node_index

    def __hash__(self):
        return hash(self._node_index)

    def _replace_references_with_nodes(
        self, list_with_references: List[Any]
    ) -> List[Any]:
        list_with_nodes: List[Any] = []
        for item in list_with_references:
            if isinstance(item, ASTNodeReference):
                list_with_nodes.append(self._create_node_from_reference(item))
            elif isinstance(item, list):
                list_with_nodes.append(self._replace_references_with_nodes(item))
            elif isinstance(item, (int, str)) or item is None:
                list_with_nodes.append(item)
            else:
                raise RuntimeError(
                    "Failed parsing attribute.\n"
                    f"An {item} with {type(item)} was found.\n"
                    "Expected: int, str, ASNodeReference of list of them."
                )

        return list_with_nodes

    def _create_node_from_reference(self, reference: ASTNodeReference) -> "ASTNode":
        return ASTNode(self._graph, reference.node_index)

    def _get_type(self, node_index: int) -> ASTNodeType:
        return self._graph.nodes[node_index]["node_type"]

    def _get_line(self, node_index: int) -> Optional[int]:
        return self._graph.nodes[node_index]["line"]

    def _get_parent(self, node_index: int) -> Optional[int]:
        # there is maximum one parent in a tree
        return next(self._graph.predecessors(node_index), None)

    # names of methods and properties, which is not generated dynamically
    _public_fixed_interface = ["children", "node_index", "line"]
