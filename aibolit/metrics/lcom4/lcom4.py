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

# import matplotlib.pyplot as plt
import networkx as nx  # type: ignore
from collections import defaultdict
from aibolit.utils.ast import AST
from typing import Set, Dict, List
from javalang.tree import ClassDeclaration, InterfaceDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node


class LCOM4:

    def value(self, filename: str) -> int:
        tree: Node = AST(filename).value()
        graph: Dict[str, Set[str]] = defaultdict(set)

        fields: List[str] = [node.declarators[0].name for _, node in tree.filter(FieldDeclaration)]
        methods: List[str] = [node.name for _, node in tree.filter(MethodDeclaration)]
        interfaces: List[InterfaceDeclaration] = [node for _, node in tree.filter(InterfaceDeclaration)]
        current_class: ClassDeclaration = list(tree.filter(ClassDeclaration))[0][1]
        interfaces_methods: Set[str] = set()
        nested_methods: Set[str] = set()

        class_decl: List[ClassDeclaration] = \
            [node for _, node in current_class.filter(ClassDeclaration) if node.name != current_class.name]

        for i in interfaces:
            interfaces_methods.update([node.name for _, node in i.filter(MethodDeclaration)])
        for k in class_decl:
            nested_methods.update([node.name for _, node in k.filter(MethodDeclaration)])

        for _, node in tree.filter(MethodDeclaration):
            for _, mem_ref in node.filter(MemberReference):
                if mem_ref.member in fields:
                    graph[node.name].add(mem_ref.member)

            for _, this_m in node.filter(This):
                graph[node.name].add(this_m.selectors[0].member)

            for _, mi in node.filter(MethodInvocation):
                if mi.member in methods:
                    graph[node.name].add(mi.member)

        return self.get_connected_components(methods, fields, graph)

    @staticmethod
    def get_connected_components(methods: list, fields: list, graph: dict) -> int:

        G = nx.Graph()

        for i in methods:
            G.add_node(i)
        for i in fields:
            G.add_node(i)
        for key, val in graph.items():
            for x in val:
                G.add_edge(key, x)

        return nx.number_connected_components(G)
