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
from collections import defaultdict
from aibolit.utils.ast import AST
from typing import Set, Dict, List, Generator, Tuple, Any
from javalang.tree import ClassDeclaration, InterfaceDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node, LocalVariableDeclaration


class LCOM4:

    def value(self, filename: str) -> int:
        tree: Node = AST(filename).value()
        graph: Dict[str, Set[str]] = defaultdict(set)

        for class_path, class_node in tree.filter(ClassDeclaration):

            field_nodes: List[Node] = list(self.filter_node_by_level(class_node, FieldDeclaration))
            field_exhaust: dict = dict(self.exhaust_field_name(field_node) for path, field_node in field_nodes)
            method_nodes: List[Node] = list(self.filter_node_by_level(class_node, MethodDeclaration))
            method_exhaust: dict = dict(self.exhaust_method_name(method_node) for path, method_node in method_nodes)


            for method_path, method_node in method_nodes:
                reference_nodes: List[Node] = list(self.filter_node_by_level(method_node, MemberReference))
                invocation_nodes: List[Node] = list(self.filter_node_by_level(method_node, MethodInvocation))
                this_nodes: List[Node] = list(self.filter_node_by_level(method_node, This))
                local_nodes: List[Node] = list(self.filter_node_by_level(method_node, LocalVariableDeclaration))
                local_exhaust: dict = dict(self.exhaust_field_name(local_node) for path, local_node in local_nodes)

                for reference_path, reference_node in reference_nodes:
                    if reference_node.member in field_exhaust and reference_node.member not in local_exhaust:
                        graph[method_node.name].add(reference_node.member)

                for this_path, this_node in this_nodes:
                    try:
                        graph[method_node.name].add(this_node.selectors[0].member)
                    except IndexError:
                        pass

                for invocation_path, invocation_node in invocation_nodes:
                    try:
                        selector_list = [{inv_selector.member: inv_selector.position} for inv_selector in
                                          invocation_node.selectors if isinstance(inv_selector, (MemberReference,
                                                                                                 MethodInvocation))]
                        qualifier_list = invocation_node.qualifier.split('.')
                        full_invocation = qualifier_list + ['*'] + selector_list
                    except (TypeError, AttributeError):
                        pass


                    '''try:
                        attribute_list = [inv_argument.member + for inv_argument in invocation_node.arguments if
                                         isinstance(inv_argument, (MemberReference, MethodInvocation))]

                    except (TypeError, AttributeError):
                        pass'''

                    if invocation_node.member in method_exhaust:
                        graph[method_node.name].add(invocation_node.member)

            methods = method_exhaust
            fields = field_exhaust
            break
        return self.get_connected_components(methods, fields, graph)

    @staticmethod
    def get_connected_components(methods, fields, graph: dict) -> int:
        G = nx.Graph()
        for field in fields:
            G.add_node(field)
        for method in methods:
            G.add_node(method)
        for key, val in graph.items():
            for x in val:
                G.add_edge(key, x)
        return nx.number_connected_components(G)

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        class_level = 0
        for step in path:
            if isinstance(step, (ClassDeclaration, InterfaceDeclaration, MethodDeclaration)):
                class_level += 1
        return class_level

    @staticmethod
    def filter_node_by_level(node: Node, javalang_class) -> Generator[Node, None, None]:
        for filtered_path, filtered_node in node.filter(javalang_class):
            if LCOM4.get_class_depth(filtered_path) == 1:
                yield filtered_path, filtered_node

    @staticmethod
    def find_method_declaration(method_name: str, method_parameters: List[Node], method_nodes: List[MethodDeclaration]):
        for method_node in method_nodes:
            if method_node.name == method_name:
                yield method_node

    def has_field(self, node: Node, field_name: str):
        node_fields = self.filter_node_by_level(node, LocalVariableDeclaration)
        field_names: List[str] = [node.declarators[0].name for path, node in node_fields]
        if field_name in field_names:
            return True
        else:
            return False

    @staticmethod
    def exhaust_method_name(method_node: Node) -> Tuple[Any, List[dict]]:
        parameter_str = '_'
        parameter_list = []
        for parameter in method_node.parameters:
            parameter_list.append({parameter.name: parameter.type.name})
        return method_node.name, parameter_list

    @staticmethod
    def exhaust_field_name(field_node: Node) -> Tuple[str, str]:
        field_type = 'None'
        try:
            field_type = field_node.type.name
        except AttributeError:
            pass
        return str(field_node.declarators[0].name), str(field_type)

    '''        def get_invocation_bounds(method_position: tuple(int, int), selector_list: List[str]) -> tuple(int, int):
            invocation_bounds = method_position
            for selector in selector_list:
                me'''
