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


from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST
from networkx import dfs_labeled_edges  # type: ignore


class NCSSMetric():
    def __init__(self):
        pass

    def value(self, filename: str):
        if len(filename) == 0:
            raise ValueError('Empty file for analysis')

        tree = AST.build_from_javalang(build_ast(filename))
        metric = 0
        for _, destination, edge_type in dfs_labeled_edges(tree.tree, tree.root):
            if edge_type == 'forward':
                node_type = str(tree.get_type(destination)).split('.')[1]
                if 'STATEMENT' in node_type and 'BLOCK_STATEMENT' not in node_type:
                    metric += 1
                elif node_type == 'CATCH_CLAUSE':
                    metric += 1
                elif 'DECLARATION' in node_type and 'PACKAGE_DECLARATION' not in node_type:
                    metric += 1

        return metric
