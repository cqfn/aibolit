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
from typing import List, Generator, Tuple, Any, Union, overload
from javalang.tree import ClassDeclaration, InterfaceDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node, LocalVariableDeclaration
FldExh = Tuple[str, Tuple[str, str]]
MthExh = Tuple[str, Tuple[Tuple[str, str], ...]]
Nodes = Tuple[tuple, Node]
NodeGen = Generator[Tuple[tuple, Node], None, None]
EdgeNode = Union[MthExh, FldExh]
JLang = Union[ClassDeclaration, InterfaceDeclaration, MethodDeclaration,
              MemberReference, FieldDeclaration, MethodInvocation, This, Node, LocalVariableDeclaration]


class LCOM4:

    def value(self, filename: str) -> int:
        tree: Node = AST(filename).value()
        G: Graph = nx.Graph()

        for class_path, class_node in tree.filter(ClassDeclaration):

            # Extract all methods and fields
            # from ClassDeclaration node

            field_nodes: List[Nodes] = list(self.filter_node_lvl(class_node, FieldDeclaration))
            full_field_exhaust: List[FldExh] = list(self.exhaust_field(field_node)
                                                    for path, field_node in field_nodes)
            clear_field_exhaust: List[FldExh] = self.clean_for_repetitions(full_field_exhaust)
            method_nodes: List[Nodes] = list(self.filter_node_lvl(class_node, MethodDeclaration))
            method_nodes: List[Nodes] = list(self.filter_getters_setters(method_nodes))  # type: ignore
            full_method_exhaust: List[MthExh] = list(self.exhaust_method(method_node)
                                                     for path, method_node in method_nodes)
            clear_method_exhaust: List[MthExh] = self.clean_for_repetitions(full_method_exhaust)

            # Add all MethodDeclarations to graph
            # Add all FieldDeclarations to graph

            for method in clear_method_exhaust:
                G.add_node(method[0] + str(hash(method[1])))
            for field in clear_field_exhaust:
                G.add_node(field[0] + str(hash(field[1])))

            # Find and compare all existing
            # MemberReferences, MethodInvocations,
            # This statements, LocalVariableDeclarations
            # to themselves and objects added to graph G

            for method_path, method_node in method_nodes:
                reference_nodes: List[Nodes] = list(self.filter_node_lvl(method_node, MemberReference))
                invocation_nodes: List[Nodes] = list(self.filter_node_lvl(method_node, MethodInvocation))
                this_nodes: List[Nodes] = list(self.filter_node_lvl(method_node, This))
                local_nodes: List[Nodes] = list(self.filter_node_lvl(method_node, LocalVariableDeclaration))
                local_exhaust: List[FldExh] = list(self.exhaust_field(local_node) for path, local_node in local_nodes)
                method_exhaust: MthExh = self.exhaust_method(method_node)
                self.add_references_to_graph(G, reference_nodes, local_exhaust, clear_field_exhaust, method_exhaust)
                self.add_this_to_graph(G, this_nodes, clear_field_exhaust, method_exhaust)
                self.add_invocations_to_graph(G, invocation_nodes, clear_method_exhaust, method_exhaust,
                                              local_exhaust, clear_field_exhaust)
            break  # Stop after first class
        return nx.number_connected_components(G)

    # ------------------------------------------------
    # Funcs for adding edges to graph

    # Filter all viable MethodInvocations and
    # compare them to existing MethodDeclarations

    def add_invocations_to_graph(self,
                                 G: Graph,
                                 invocation_nodes: List[Nodes],
                                 full_method_exhaust: List[MthExh],
                                 method_exhaust: MthExh,
                                 local_exhaust: List[FldExh],
                                 full_field_exhaust: List[FldExh]) -> None:
        for invocation_path, invocation_node in invocation_nodes:
            if isinstance(invocation_node.selectors, list):  # Check for inv being first in whole statement
                for method in full_method_exhaust:
                    if invocation_node.member == method[0]:
                        self.add_vertices_edges(G, 'invocation', method_exhaust, method)
                inv_arguments = self.get_arguments(invocation_node)
                inv_fields: List[str] = inv_arguments[1]
                inv_funcs: List[str] = inv_arguments[0]
                if len(inv_fields) > 0:
                    self.add_invocation_fields(G, inv_fields, local_exhaust, full_field_exhaust, method_exhaust)
                if len(inv_funcs) > 0:
                    self.add_invocation_funcs(G, inv_funcs, full_method_exhaust, method_exhaust)

    # Filter all viable invocation attributes and
    # compare them to existing FieldDeclarations

    def add_invocation_fields(self,
                              G: Graph,
                              inv_fields: List[str],
                              local_exhaust: List[FldExh],
                              full_field_exhaust: List[FldExh],
                              method_exhaust: MthExh) -> None:
        for inv_argument in inv_fields:
            if inv_argument not in [x[0] for x in local_exhaust]:
                for field in full_field_exhaust:
                    if inv_argument == field[0]:
                        self.add_vertices_edges(G, 'reference', method_exhaust, field)

    # Filter all viable invocation attributes and
    # compare them to existing MethodDeclarations

    def add_invocation_funcs(self,
                             G: Graph,
                             inv_funcs: Tuple[str],
                             full_method_exhaust: List[MthExh],
                             method_exhaust: MthExh) -> None:
        for inv_argument in inv_funcs:  # ToDo: make a func for a return type check
            for method in full_method_exhaust:
                if inv_argument == method[0]:
                    self.add_vertices_edges(G, 'reference', method_exhaust, method)

    # Filter all viable member references and
    # compare them to existing FieldDeclarations

    def add_references_to_graph(self,
                                G: Graph,
                                reference_nodes: List[Nodes],
                                local_exhaust: List[FldExh],
                                full_field_exhaust: List[FldExh],
                                method_exhaust: MthExh) -> None:
        for reference_path, reference_node in reference_nodes:
            if isinstance(reference_node.selectors, list):  # Check for node being "alone"
                if reference_node.member not in [x[0] for x in local_exhaust]:
                    for field in full_field_exhaust:
                        if reference_node.member == field[0]:
                            self.add_vertices_edges(G, 'ref', method_exhaust, field)

    # Filter all viable This statements and
    # compare them to existing FieldDeclarations

    def add_this_to_graph(self,
                          G: Graph,
                          this_nodes: List[Nodes],
                          full_field_exhaust: List[FldExh],
                          method_exhaust: MthExh) -> None:
        for this_path, this_node in this_nodes:
            for field in full_field_exhaust:
                if len(this_node.selectors) == 1 and isinstance(this_node.selectors[0], MemberReference):
                    if this_node.selectors[0].member in field:
                        self.add_vertices_edges(G, 'this.', method_exhaust, field)

    # Add given objects to the graph as
    # nodes and add an edge between.

    @staticmethod
    def add_vertices_edges(G, edge_type: str, first_node: EdgeNode, second_node: EdgeNode) -> None:
        G.add_node(first_node[0] + str(hash(first_node[1])))                                 # Add nodes and edges with
        G.add_node((second_node[0]) + str(hash(second_node[1])))                             # given nodes
        G.add_edge(first_node[0] + str(hash(first_node[1])),
                   (second_node[0]) + str(hash(second_node[1])), type=edge_type)

    # ------------------------------------------------
    # Funcs for filtering nodes

    # Filter given node
    # by their level of nesting.
    # If node is inside nested method, class or interface –
    # ignore it
    # gets rid of it

    @staticmethod
    def filter_node_lvl(node: Node, javalang_class) -> NodeGen:
        for filtered_path, filtered_node in node.filter(javalang_class):
            if LCOM4.get_class_depth(filtered_path) == 1:
                yield filtered_path, filtered_node

    # Filter given list of MethodDeclaration nodes
    # by their name. if node's name starts with 'set'/'get' –
    # gets rid of it

    @staticmethod
    def filter_getters_setters(method_node_list: List[Tuple[tuple, Node]]) -> NodeGen:
        for path, node in method_node_list:                     # ToDo: implement get/set detection with .body
            if node.name.startswith(('get', 'set')):            # type: ignore
                pass
            else:
                yield path, node

    # Get level of nesting by Class, Interface of Method
    # for given node
    #
    # returns an int indicating level of nesting

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        class_level = 0
        for step in path:
            if isinstance(step, (ClassDeclaration, InterfaceDeclaration, MethodDeclaration)):
                class_level += 1
        return class_level

    # Extracts name and argument's names and types
    # for given MethodDeclaration node
    #
    # javacode example:
    # public void doNothing(int a, float b, string c) {}
    # returns (doNothing, ((a, int), (b, float), (c, string)))

    @staticmethod
    def exhaust_method(method_node: Node) -> MthExh:
        parameter_list = []
        name: str = method_node.name  # type: ignore
        for parameter in method_node.parameters:  # type: ignore
            parameter_list.append((parameter.name, parameter.type.name))
        parameter_tuple: Tuple[Tuple[str, str], ...] = tuple(parameter_list)
        return name, parameter_tuple

    # Extracts name and type for given FieldDeclaration node
    #
    # javacode example:
    # int a;
    # returns (a, (type, int))

    @staticmethod
    def exhaust_field(field_node: Node) -> FldExh:  # ToDo: get rid of 'type' in parameter_tuple
        name = field_node.declarators[0].name  # type: ignore
        try:
            parameter_tuple: Tuple[str, str] = ('type', field_node.type.name)  # type: ignore
        except AttributeError:
            return "", ("", "")
        return name, parameter_tuple

    # Get every argument from method invocation,
    # return two lists with attributes and methods
    #
    # javacode example:
    # foo(int a, float b, bar()):{}
    # returns ([a,b], [bar])

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

    @staticmethod  # Clean any list from repetitions
    def clean_for_repetitions(list_of_exhaust: List[Any]) -> List[Any]:
        for item in list_of_exhaust:
            if list_of_exhaust.count(item) > 1:
                list_of_exhaust.remove(item)
        return list_of_exhaust
