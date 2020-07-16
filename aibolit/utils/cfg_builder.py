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

from networkx import DiGraph, disjoint_union  # type: ignore
from aibolit.ast_framework import AST, ASTNodeType
from typing import Tuple


NODE_TYPES = [
    ASTNodeType.ASSIGNMENT,
    ASTNodeType.RETURN_STATEMENT
]


def build_cfg(tree: AST) -> DiGraph:
    '''Create Control Flow Graph'''
    g = DiGraph()
    g.add_node(0)
    for node in tree:
        if node.node_type not in NODE_TYPES:
            continue
        _g = _mk_cfg_graph(node.node_type)
        g = _compose_two_graphs(g, _g)
    return g


def _mk_cfg_graph(node: ASTNodeType) -> Tuple[DiGraph, int]:
    '''Takes in Javalang statement and returns corresponding CFG'''
    g = DiGraph()
    g.add_node(0)
    return g


def _compose_two_graphs(g1: DiGraph, g2: DiGraph) -> DiGraph:
    '''Compose two graphs by creating the edge between last of the fist graph and fist of the second.
       We assume that node in the each graph G has order from 0 to len(G)-1
    '''
    g = disjoint_union(g1, g2)
    g.add_edge(len(g1) - 1, len(g1))
    return g
