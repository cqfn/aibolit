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

import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved, VarMiddle
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from collections import defaultdict
class PartialSync:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        """
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def value(self, filename):
        # tree = self.__file_to_ast(filename)
        total_code_lines = set()
        obj = JavalangImproved(filename)
        # empty_lines = tree.get_empty_lines()
        items = obj.tree_to_nodes()
        synch_nodes = defaultdict(list)
        method_nodes = []
        for x in items:
            if isinstance(x.node, javalang.tree.SynchronizedStatement):
                synch_nodes[x.method_line].append(x)
            elif isinstance(x.node, javalang.tree.MethodDeclaration):
                method_nodes.append(x)

        # pattern = re.compile(r'(?<=([\w])\+)\"[\w]+\"')
        for method_node in method_nodes:
            # method_statements = [node for _, node in method_node.filter(javalang.tree.StatementExpression)]
            lst_nodes = [lst for lst in method_node.node.children if isinstance(lst, list) and lst]
            # exclude list of FormalParameter items, it is the first item always
            method_statements = lst_nodes[1]
            after_synch_statements = 0
            statement_number = 0
            sync_node = None
            for node in method_statements:
                if not isinstance(node, javalang.tree.SynchronizedStatement):
                    after_synch_statements += 1
                else:
                    statement_number += 1
                    sync_node = synch_nodes[method_node.node.position.line][statement_number - 1]
            if after_synch_statements != len(method_statements):
                total_code_lines.add(sync_node.line)
            # for _, sync_node in method_node.filter(javalang.tree.SynchronizedStatement):
            #     sync_statements = [node for _, node in sync_node.filter(javalang.tree.StatementExpression)]
            #     if len(method_statements) != len(sync_statements):
            #         if not hasattr(sync_node.children[1].position, 'line'):
            #             total_code_lines.add(sync_node.children[1].position.line)
            #         else:
            #             total_code_lines.add(sync_node.children[1].position.line)
            #     print('{} {} method stat length {}, sync stat length {}'.format(
            #         filename.name,
            #         method_node.name,
            #         len(method_statements),
            #         len(sync_statements)))

        return sorted(total_code_lines)

import pathlib
partS = PartialSync()
for path in pathlib.Path(r'D:\git\aibolit\test\patterns\partial_synchronized').iterdir():
    if path.is_file() and path.name.endswith('java'):
        print(path, partS.value(path))