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

from typing import List, Dict, Set, Iterator

from networkx import DiGraph, strongly_connected_components, weakly_connected_components  # type: ignore

from aibolit.ast_framework import AST
from aibolit.ast_framework.java_class import JavaClass


def decompose_java_class(java_class: JavaClass, strength: str) -> List[AST]:
    '''
    Splits java_class fields and methods by their usage and
    construct for each case an AST with only those fields and methods kept.
    Use "strength" parameter to control splitting criteria. Use "strong" or "weak"
    for splitting fields and methods by strong and weak connectivity.
    '''
    usage_graph = DiGraph()
    fields_ids: Dict[str, int] = {}
    methods_ids: Dict[str, int] = {}
    for field_name in java_class.fields:
        fields_ids[field_name] = len(fields_ids)
        usage_graph.add_node(fields_ids[field_name], type='field', name=field_name)
    for method_name in java_class.methods:
        methods_ids[method_name] = len(fields_ids) + 1 + len(methods_ids)
        usage_graph.add_node(methods_ids[method_name], type='method', name=method_name)

    for method_name in java_class.methods:
        for method in java_class.methods[method_name]:
            for used_field_name in method.used_fields:
                usage_graph.add_edge(methods_ids[method_name], fields_ids[used_field_name])
            for used_method_name in method.used_methods:
                usage_graph.add_edge(methods_ids[method_name], methods_ids[used_method_name])

    components: Iterator[Set[int]]
    if strength == 'strong':
        components = strongly_connected_components(usage_graph)
    elif strength == 'weak':
        components = weakly_connected_components(usage_graph)
    else:
        raise ValueError(f'"strength" argument must be either "strong" or "weak", but "{strength}" was provided.')

    class_parts: List[AST] = []
    for component in components:
        field_names = [usage_graph.nodes[node]['name'] for node in component
                       if usage_graph.nodes[node]['type'] == 'field']
        method_names = [usage_graph.nodes[node]['name'] for node in component
                        if usage_graph.nodes[node]['type'] == 'method']
        class_parts.append(_filter_class_methods_and_fields(java_class, field_names, method_names))

    return class_parts


def _filter_class_methods_and_fields(java_class: JavaClass, allowed_fields_names: List[str],
                                     allowed_methods_names: List[str]) -> AST:
    allowed_nodes = {java_class.root}
    for field_name in allowed_fields_names:
        field = java_class.fields[field_name]
        allowed_nodes |= field.tree.nodes
    for method_name in allowed_methods_names:
        for method in java_class.methods[method_name]:
            allowed_nodes |= method.tree.nodes

    return AST(java_class.tree.subgraph(allowed_nodes), java_class.root)
