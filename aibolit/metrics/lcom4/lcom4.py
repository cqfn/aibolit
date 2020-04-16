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
import networkx as nx
import matplotlib.pyplot as plt

class LCOM4():

    def __init__(self):
        pass

    def value(self, filename: str):
        G = nx.Graph()
        G.add_node('this.a')
        G.add_node('method1')
        G.add_node('method2')
        G.add_node('this.b')
        G.add_edge('this.b', 'method1')
        G.add_edges_from([['this.a', 'method2'], ['method2', 'method1']])
        # nx.draw(G,with_labels=True)
        # plt.show()
        return 0


# LCOM4().value('')
import javalang
with open(r'D:\temp\silvercase\aibolit\test\metrics\lcom4\Simple.java', encoding='utf-8') as f:
    t = javalang.parse.parse(f.read())
    from collections import defaultdict
    graph = defaultdict(set)
    methods = [node.name for _, node in t.filter(javalang.tree.MethodDeclaration)]
    interfaces = [node for _, node in t.filter(javalang.tree.InterfaceDeclaration)]
    interfaces_methods = set()
    for i in interfaces:
        interfaces_methods.update([node.name for _, node in i.filter(javalang.tree.MethodDeclaration)])

    current_class = list(t.filter(javalang.tree.ClassDeclaration))[0][1]
    class_decl = [node for _, node in current_class.filter(javalang.tree.ClassDeclaration) if node.name != current_class.name]
    nested_methods = set()
    for i in class_decl:
        nested_methods.update([node.name for _, node in i.filter(javalang.tree.MethodDeclaration)])
    total_methods = set(methods).difference(interfaces_methods.union(nested_methods))
    fields = [node.declarators[0].name for _, node in t.filter(javalang.tree.FieldDeclaration)]

    for _, node in t.filter(javalang.tree.MethodDeclaration):
        for _, mem_ref in node.filter(javalang.tree.MemberReference):
            if mem_ref.member in fields:
                graph[node.name].add(mem_ref.member)

        for _, this_m in node.filter(javalang.tree.This):
            graph[node.name].add(this_m.selectors[0].member)

        for _, mi in node.filter(javalang.tree.MethodInvocation):
            if mi.member in methods:
                graph[node.name].add(mi.member)


    # t.add_node
    # for key, val in graph.items():
    #     for i in val:
    #         graph.addEdge(key, i)
    #
    # g = list(t.filter(javalang.tree.MemberReference))
    # print(g)