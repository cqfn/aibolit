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

import networkx as nx  # type: ignore
from networkx import Graph
from aibolit.utils.ast import AST
from typing import List, Generator, Tuple, Any
from javalang.tree import ClassDeclaration, InterfaceDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node, LocalVariableDeclaration


class LCOM4:

    def value(self, filename: str) -> int:
        tree: Node = AST(filename).value()
        G: Graph = nx.Graph()

        for class_path, class_node in tree.filter(ClassDeclaration):

            field_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(class_node, FieldDeclaration))
            full_field_exhaust: List[Tuple[str, Tuple[str, str]]] = list(self.exhaust_field(field_node) for
                                                                         path, field_node in field_nodes)
            clear_field_exhaust: List[Tuple[str, Tuple[str, str]]] = self.clean_for_repetitions(full_field_exhaust)
            method_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(class_node, MethodDeclaration))
            method_nodes: List[Tuple[tuple, Node]] = list(self.filter_getters_setters(method_nodes))  # type: ignore
            full_method_exhaust: List[Tuple[str, Tuple[Tuple[str, str], ...]]] = \
                list(self.exhaust_method(method_node) for path, method_node in method_nodes)
            clear_method_exhaust: List[Tuple[str, Tuple[Tuple[str, str], ...]]] = \
                self.clean_for_repetitions(full_method_exhaust)

            for method in clear_method_exhaust:
                G.add_node(method[0] + str(hash(method[1])))
            for field in clear_field_exhaust:
                G.add_node(field[0] + str(hash(field[1])))

            for method_path, method_node in method_nodes:
                reference_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(method_node, MemberReference))
                invocation_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(method_node, MethodInvocation))
                this_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(method_node, This))
                local_nodes: List[Tuple[tuple, Node]] = list(self.filter_node_lvl(method_node,
                                                                                  LocalVariableDeclaration))
                local_exhaust: List[Tuple[str, Tuple[str, str]]] = list(self.exhaust_field(local_node) for path,
                                                                        local_node in local_nodes)
                method_exhaust: Tuple[str, Tuple[Tuple[str, str], ...]] = self.exhaust_method(method_node)
                self.add_references_to_graph(G, reference_nodes, local_exhaust, clear_field_exhaust, method_exhaust)
                self.add_this_to_graph(G, this_nodes, clear_field_exhaust, method_exhaust)
                self.add_invocations_to_graph(G, invocation_nodes, clear_method_exhaust, method_exhaust,
                                              local_exhaust, clear_field_exhaust)
            break  # Stop after first class
        return nx.number_connected_components(G)

    # ------------------------------------------------
    # Funcs for adding edges to graph

    def add_invocations_to_graph(self, G, invocation_nodes, full_method_exhaust, method_exhaust, local_exhaust,
                                 full_field_exhaust):
        for invocation_path, invocation_node in invocation_nodes:
            if isinstance(invocation_node.selectors, list):  # Check for inv being first in whole statement
                for method in full_method_exhaust:
                    if invocation_node.member == method[0]:
                        self.add_vertices_edges(G, 'invocation', method_exhaust, method)
                inv_arguments = self.get_arguments(invocation_node)
                inv_fields = inv_arguments[1]
                inv_funcs = inv_arguments[0]
                if len(inv_fields) > 0:
                    self.add_invocation_fields(G, inv_fields, local_exhaust, full_field_exhaust, method_exhaust)
                if len(inv_funcs) > 0:
                    self.add_invocation_funcs(G, inv_funcs, full_method_exhaust, method_exhaust)

    def add_invocation_fields(self, G, inv_fields, local_exhaust, full_field_exhaust, method_exhaust):
        for inv_argument in inv_fields:
            if inv_argument not in [x[0] for x in local_exhaust]:
                for field in full_field_exhaust:
                    if inv_argument == field[0]:
                        self.add_vertices_edges(G, 'reference', method_exhaust, field)

    def add_invocation_funcs(self, G, inv_funcs, full_method_exhaust, method_exhaust):
        for inv_argument in inv_funcs:  # ToDo: make a func for a return type check
            for method in full_method_exhaust:
                if inv_argument == method[0]:
                    self.add_vertices_edges(G, 'reference', method_exhaust, method)

    def add_references_to_graph(self, G, reference_nodes, local_exhaust, full_field_exhaust, method_exhaust):
        for reference_path, reference_node in reference_nodes:
            if isinstance(reference_node.selectors, list):  # Check for node being "alone"
                if reference_node.member not in [x[0] for x in local_exhaust]:
                    for field in full_field_exhaust:
                        if reference_node.member == field[0]:
                            self.add_vertices_edges(G, 'ref', method_exhaust, field)

    def add_this_to_graph(self, G, this_nodes, full_field_exhaust, method_exhaust):
        for this_path, this_node in this_nodes:
            for field in full_field_exhaust:
                if len(this_node.selectors) == 1 and isinstance(this_node.selectors[0], MemberReference):
                    if this_node.selectors[0].member in field:
                        self.add_vertices_edges(G, 'this.', method_exhaust, field)

    @staticmethod
    def add_vertices_edges(G, edge_type: str, first_node, second_node):  # Add nodes and edges with given nodes
        G.add_node(first_node[0] + str(hash(first_node[1])))
        G.add_node((second_node[0]) + str(hash(second_node[1])))
        G.add_edge(first_node[0] + str(hash(first_node[1])),
                   (second_node[0]) + str(hash(second_node[1])), type=edge_type)

    # ------------------------------------------------
    # Funcs for filtering nodes

    @staticmethod
    def filter_node_lvl(node: Node, javalang_class) -> Generator[Tuple[tuple, Node], None, None]:
        for filtered_path, filtered_node in node.filter(javalang_class):
            if LCOM4.get_class_depth(filtered_path) == 1:
                yield filtered_path, filtered_node

    @staticmethod
    def filter_getters_setters(method_node_list: List[Tuple[tuple, Node]]) -> Generator[Tuple[tuple, Node], None, None]:
        for path, node in method_node_list:                     # ToDo: implement get/set detection with .body
            if node.name.startswith(('get', 'set')):            # type: ignore
                pass
            else:
                yield path, node

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        class_level = 0
        for step in path:
            if isinstance(step, (ClassDeclaration, InterfaceDeclaration, MethodDeclaration)):
                class_level += 1
        return class_level

    @staticmethod
    def exhaust_method(method_node: Node) -> Tuple[str, Tuple[Tuple[str, str], ...]]:
        parameter_list = []
        name: str = method_node.name  # type: ignore
        for parameter in method_node.parameters:  # type: ignore
            parameter_list.append((parameter.name, parameter.type.name))
        parameter_tuple: Tuple[Tuple[str, str], ...] = tuple(parameter_list)
        return name, parameter_tuple

    @staticmethod
    def exhaust_field(field_node: Node) -> Tuple[str, Tuple[str, str]]:
        name = field_node.declarators[0].name  # type: ignore
        try:
            parameter_list: Tuple[str, str] = ('type', field_node.type.name)  # type: ignore
        except AttributeError:
            return "", ("", "")
        return name, parameter_list

    @staticmethod
    def get_arguments(invocation_node: Node) -> Tuple[List[str], List[str]]:
        list_of_funcs = []
        list_of_fields = []
        for argument in invocation_node.arguments:  # type: ignore
            if isinstance(argument, MethodInvocation):
                list_of_funcs.append(argument.member)
            elif isinstance(argument, MemberReference):
                list_of_fields.append(argument.member)
        return list_of_funcs, list_of_fields

    @staticmethod
    def clean_for_repetitions(list_of_exhaust: List[Any]) -> List[Any]:
        for item in list_of_exhaust:
            if list_of_exhaust.count(item) > 1:
                list_of_exhaust.remove(item)
        return list_of_exhaust
