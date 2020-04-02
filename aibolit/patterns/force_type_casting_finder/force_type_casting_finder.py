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
from aibolit.utils.ast import AST


class ForceTypeCastingFinder:

    def __process_node(self, node):
        line = node.position.line if hasattr(node, 'position') and node.position is not None else None
        qualifier = node.qualifier if hasattr(node, 'qualifier') else None
        member = node.member if hasattr(node, 'member') else None
        name = node.name if hasattr(node, 'name') else None
        return {
            "line": line,
            "name": qualifier or member or name,
            "ntype": type(node)
        }

    def __tree_to_list(self, tree: javalang.tree.CompilationUnit):
        '''Convert AST tree to list of object'''
        items = [self.__process_node(node) for path, node in tree if node is not None]

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
        tree = AST(filename).value()
        list_tree = self.__tree_to_list(tree)
        num_str = []
        for node in list_tree:
            if node['ntype'] == javalang.tree.Cast:
                k = int(node['line'])
                if k not in num_str:
                    num_str.append(k)
        return num_str
