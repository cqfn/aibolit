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
from networkx import Graph  # type: ignore
from aibolit.utils.ast import AST
from aibolit.utils.cohesiongraph import CohesionGraph
from aibolit.utils.filter import Filters
from javalang.tree import Node
from typing import List


class LCOM5:

    coh = CohesionGraph()

    def __init__(self):
        pass

    def value(self, filename: str) -> float:

        attribute_list: List[str] = []
        method_list: List[str] = []
        num_of_references: int = 0

        tree: Node = AST(filename).value()
        G: Graph = self.coh.value(tree)
        for (u, v, c) in G.edges.data('type'):
            if c == 'invocation':
                method_list.append(u)
                method_list.append(v)
            if c == 'reference':
                method_list.append(u)
                attribute_list.append(v)
                num_of_references += 1

        attribute_list = Filters.clean_for_repetitions(attribute_list)
        method_list = Filters.clean_for_repetitions(method_list)
        attr_cnt = len(attribute_list)
        mth_cnt = len(method_list)
        ref_cnt = num_of_references

        try:
            result: float = (ref_cnt - mth_cnt * attr_cnt) / (attr_cnt - mth_cnt * attr_cnt)
        except ZeroDivisionError:
            return 0.0
        return result
