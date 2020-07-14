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

from typing import List, Iterator

from networkx import DiGraph  # type: ignore

from aibolit.ast_framework._auxiliary_data import common_attributes, attributes_by_node_type, ASTNodeReference


class ASTNode:
    def __init__(self, graph: DiGraph, node_index: int):
        self._graph = graph
        self._node_index = node_index

    def __dir__(self) -> List[str]:
        node_type = self._graph.nodes[self._node_index]['node_type']
        return ['children'] + list(common_attributes) + list(attributes_by_node_type[node_type])

    @property
    def children(self) -> Iterator['ASTNode']:
        for child_index in self._graph.succ[self._node_index]:
            yield ASTNode(self._graph, child_index)

    def __getattr__(self, attribute_name: str):
        if attribute_name not in common_attributes:
            node_type = self._graph.nodes[self._node_index]['node_type']
            if(attribute_name not in attributes_by_node_type[node_type]):
                raise AttributeError(f'{node_type} node does not have "{attribute_name}" attribute.')

        attribute = self._graph.nodes[self._node_index][attribute_name]
        if isinstance(attribute, ASTNodeReference):
            attribute = ASTNode(self._graph, attribute.node_index)
        elif isinstance(attribute, list) and \
                all((isinstance(item, ASTNodeReference) for item in attribute)):
            attribute = [ASTNode(self._graph, item.node_index) for item in attribute]
        return attribute

    def __str__(self) -> str:
        text_representation = f'node index: {self._node_index}'
        node_type = self.__getattr__('node_type')
        for attribute_name in sorted(common_attributes | attributes_by_node_type[node_type]):
            text_representation += f'\n{attribute_name}: {self.__getattr__(attribute_name)}'

        return text_representation

    def __repr__(self) -> str:
        return f'<ASTNode node_type: {self.__getattr__("type")}, node_index: {self._node_index}>'
