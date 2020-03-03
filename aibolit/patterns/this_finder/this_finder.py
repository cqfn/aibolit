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


class ThisFinder:
    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def __process_node(self, node):
        line = node.position.line if hasattr(node, 'position') and node.position is not None else None
        name = node.name if hasattr(node, 'name') else None
        return {
            "line": line,
            "ntype": type(node)
        }

    def __tree_to_list(self, tree: javalang.tree.CompilationUnit):
        '''Convert AST tree to list of object'''
        items = [self.__process_node(node) for path, node in tree if node is not None]
        return items
        # fill missed line numbers
        last_line_number = None

        for item in items:
            if (item['line']) is not None:
                last_line_number = item['line']
                continue
            item['line'] = last_line_number

        return items

    def value(self, filename: str):
        ''''''
        tree = self.__file_to_ast(filename)
        list_tree = self.__tree_to_list(tree)
        num_str = []
        n = len(list_tree)
        flag = 0
        number = 0
        types = [javalang.tree.ConstructorDeclaration, javalang.tree.MethodDeclaration, javalang.tree.ClassDeclaration]
        for i in range(n):
            node = list_tree[i]
            if node['ntype'] == javalang.tree.ConstructorDeclaration:
                number = node['line']
                flag = 0
            if node['ntype'] == javalang.tree.MethodDeclaration:
                flag = 0
            if node['ntype'] == javalang.tree.ExplicitConstructorInvocation:
                flag = 1
                if list_tree[i - 2]['ntype'] == javalang.tree.Literal:
                    num_str.append(number)
            if node['ntype'] == javalang.tree.Literal and flag:
                if i == n - 1:
                    pass
                elif list_tree[i + 1]['ntype'] not in types:
                    num_str.append(number)
                flag = 0
        return sorted(list(set(num_str)))
