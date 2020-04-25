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
import matplotlib.pyplot as plt
import networkx as nx  # type: ignore
from collections import defaultdict, namedtuple
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
            full_field_exhaust = list(self.exhaust_field_name(field_node) for path, field_node in field_nodes)
            full_field_exhaust = self.clean_for_repetitions(full_field_exhaust)
            method_nodes: List[Node] = list(self.filter_node_by_level(class_node, MethodDeclaration))
            full_method_exhaust = list(self.exhaust_method_name(method_node) for path, method_node in method_nodes)
            full_method_exhaust = self.clean_for_repetitions(full_method_exhaust)

            G = nx.Graph()

            for method in full_method_exhaust:
                G.add_node(method[0] + str(hash(method[1])))
            for field in full_field_exhaust:
                G.add_node(field[0] + str(hash(field[1])))
            pass
            for method_path, method_node in method_nodes:
                reference_nodes: List[Node] = list(self.filter_node_by_level(method_node, MemberReference))
                invocation_nodes: List[Node] = list(self.filter_node_by_level(method_node, MethodInvocation))
                this_nodes: List[Node] = list(self.filter_node_by_level(method_node, This))
                local_nodes: List[Node] = list(self.filter_node_by_level(method_node, LocalVariableDeclaration))
                local_exhaust = list(self.exhaust_field_name(local_node) for path, local_node in local_nodes)
                method_exhaust = self.exhaust_method_name(method_node)

                for reference_path, reference_node in reference_nodes:
                    if isinstance(reference_node.selectors, list):
                        for field in full_field_exhaust:
                            for local_attribute in local_exhaust:
                                if reference_node.member != local_attribute[0] and reference_node.member == field[0]:
                                    G.add_node(method_exhaust[0] + str(hash(method_exhaust[1])))
                                    G.add_node((field[0]) + str(hash(field[1])))
                                    G.add_edge(method_exhaust[0] + str(hash(method_exhaust[1])),
                                               (field[0]) + str(hash(field[1])), type='ref')

                for this_path, this_node in this_nodes:
                    for field in full_field_exhaust:
                        if len(this_node.selectors) == 1 and isinstance(this_node.selectors[0], MemberReference):
                            if this_node.selectors[0].member in field:
                                G.add_node(method_exhaust[0] + str(hash(method_exhaust[1])))
                                G.add_node((field[0]) + str(hash(field[1])))
                                G.add_edge(method_exhaust[0] + str(hash(method_exhaust[1])), (field[0]) +
                                           str(hash(field[1])), type='this.')

                for invocation_path, invocation_node in invocation_nodes:
                    if isinstance(invocation_node.selectors, list):  # Check for inv being first in whole statement
                        inv_chain = self.exhaust_invocation(invocation_node)
                        if not len(inv_chain) > 0:  # Ignore all chain methods
                            for method in full_method_exhaust:
                                if invocation_node.member == method[0]:
                                    G.add_node(method[0] + str(hash(method[1])))
                                    G.add_node((method_exhaust[0]) + str(hash(method_exhaust[1])))
                                    G.add_edge(method_exhaust[0] + str(hash(method_exhaust[1])),
                                               method[0] + str(hash(method[1])), type='invocation.')

                            inv_arguments = self.get_arguments(invocation_node)
                            inv_fields = inv_arguments[1]
                            inv_funcs = inv_arguments[0]
                            if len(inv_fields) > 0:
                                for inv_argument in inv_fields:
                                    for field in full_field_exhaust:
                                        if inv_argument == field[0]:
                                            G.add_node(method_exhaust[0] + str(hash(method_exhaust[1])))
                                            G.add_node((field[0]) + str(hash(field[1])))
                                            G.add_edge(method_exhaust[0] + str(hash(method_exhaust[1])),
                                                       (field[0]) + str(hash(field[1])), type='reference')
                            if len(inv_funcs) > 0:
                                for inv_argument in inv_funcs:
                                    for method in full_method_exhaust:
                                        if inv_argument == method[0]:
                                            G.add_node(method_exhaust[0] + str(hash(method_exhaust[1])))
                                            G.add_node((method[0]) + str(hash(method[1])))
                                            G.add_edge(method_exhaust[0] + str(hash(method_exhaust[1])),
                                                       (method[0]) + str(hash(method[1])), type='reference')



            #nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
            #plt.show()
            break
        return nx.number_connected_components(G)

    @staticmethod
    def filter_node_by_level(node: Node, javalang_class) -> Generator[Node, None, None]:
        for filtered_path, filtered_node in node.filter(javalang_class):
            if LCOM4.get_class_depth(filtered_path) == 1:
                yield filtered_path, filtered_node

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        class_level = 0
        for step in path:
            if isinstance(step, (ClassDeclaration, InterfaceDeclaration, MethodDeclaration)):
                class_level += 1
        return class_level

    @staticmethod
    def find_method_declaration(method_name: str, method_parameters: List[Node], method_nodes: List[MethodDeclaration]):
        for method_node in method_nodes:
            if method_node.name == method_name:
                yield method_node

    def has_field(self, field_name: str, method_node: MethodDeclaration):
        node_fields = self.filter_node_by_level(method_node, LocalVariableDeclaration)
        field_names: List[str] = [local_node.declarators[0].name for path, local_node in node_fields]
        if field_name in field_names:
            return True
        else:
            return False

    @staticmethod
    def exhaust_method_name(method_node: Node) -> Tuple[Any, List[dict]]:
        parameter_list = []
        name = method_node.name
        for parameter in method_node.parameters:
            parameter_list.append((parameter.name, parameter.type.name))
        return name, tuple(parameter_list)

    @staticmethod
    def exhaust_field_name(field_node: Node) -> Tuple[str, str]:
        name = field_node.declarators[0].name
        parameter_list = []
        try:
            parameter_list = ('type', field_node.type.name)
        except AttributeError:
            pass
        return name, parameter_list

    @staticmethod
    def get_node_path(node: Node):
        node_path = ''
        if isinstance(node, (MethodInvocation, MemberReference)):
            node_path += node.qualifier
            for selector in node.selectors:
                node_path += selector.member
        return node_path

    @staticmethod
    def exhaust_invocation(invocation_node):
        try:
            selector_list = [inv_selector.member for inv_selector in invocation_node.selectors if
                             isinstance(inv_selector, (MemberReference, MethodInvocation))]
            qualifier_list = [qualifier for qualifier in invocation_node.qualifier.split('.') if qualifier != '']
            full_invocation = qualifier_list + selector_list
            return full_invocation
        except (TypeError, AttributeError):
            return []

    @staticmethod
    def get_arguments(invocation_node):
        list_of_funcs = []
        list_of_fields = []

        for argument in invocation_node.arguments:
            if isinstance(argument, MethodInvocation):
                list_of_funcs.append(argument.member)
            elif isinstance(argument, MemberReference):
                list_of_fields.append(argument.member)
        return list_of_funcs, list_of_fields

    @staticmethod
    def clean_for_repetitions(list):
        for item in list:
            if list.count(item) > 1:
                list.remove(item)
        return list