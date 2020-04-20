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
from typing import Set, Dict, List, Generator
from javalang.tree import ClassDeclaration, MethodDeclaration, \
    MemberReference, FieldDeclaration, MethodInvocation, This, Node


class LCOM4:

    def value(self, filename: str) -> int:
        tree: Node = AST(filename).value()
        graph: Dict[str, Set[str]] = defaultdict(set)
        fields: List[str] = []
        methods: List[str] = []
        fields += list(self.filter_field_name(tree, FieldDeclaration))

        methods += list(self.filter_method_name(tree, MethodDeclaration))

        for path, node in tree.filter(MethodDeclaration):
            if self.get_class_depth(path) < 2:
                for ref_path, mem_ref in node.filter(MemberReference):
                    if mem_ref.member in fields:
                        graph[node.name].add(mem_ref.member)

            for this_path, this_m in node.filter(This):
                try:
                    graph[node.name].add(this_m.selectors[0].member)
                except IndexError:
                    pass

            for invo_path, mi in node.filter(MethodInvocation):
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

    @staticmethod
    def get_class_depth(path: tuple) -> int:
        class_level = 0
        for step in path:
            if isinstance(step, ClassDeclaration):
                class_level += 1
        return class_level

    @staticmethod
    def filter_method_name(tree: Node, javalang_class: FieldDeclaration) -> Generator[str, None, None]:
        for path, node in tree.filter(javalang_class):
            if LCOM4.get_class_depth(path) < 2:
                yield node.name

    @staticmethod
    def filter_field_name(tree: Node, javalang_class: MethodDeclaration) -> Generator[str, None, None]:
        for path, node in tree.filter(javalang_class):
            if LCOM4.get_class_depth(path) < 2:
                yield node.declarators[0].name
