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

from collections import defaultdict

import javalang

from aibolit.patterns.var_middle.var_middle import JavalangImproved


class PartialSync:

    def __init__(self):
        pass

    def value(self, filename):
        total_code_lines = set()
        obj = JavalangImproved(filename)
        empty_lines = obj.get_empty_lines()
        items = obj.tree_to_nodes()
        synch_nodes = defaultdict(list)
        method_nodes = {}

        for x in items:
            is_instance_sync_stat = isinstance(x.node, javalang.tree.SynchronizedStatement)
            is_instance_method_decl = isinstance(x.node, javalang.tree.MethodDeclaration)
            is_instance_ctr = isinstance(x.node, javalang.tree.ConstructorDeclaration)
            is_instance_lambda = isinstance(x.node, javalang.tree.LambdaExpression)

            if is_instance_sync_stat:
                synch_nodes[x.method_line].append(x)
            elif is_instance_method_decl or is_instance_ctr or is_instance_lambda:
                method_nodes[x.method_line] = x

        for method_line, sync_nodes in sorted(synch_nodes.items(), key=lambda x: x[1][0].line):
            for sync_n in sync_nodes:
                lines = set(range(method_line, sync_n.line))
                empty_lines_before_sync = [x for x in lines if x in empty_lines]
                lines_number_btw_function_and_synch_block = sync_n.line - method_line - len(
                    empty_lines_before_sync)
                if lines_number_btw_function_and_synch_block > 1:
                    total_code_lines.add(sync_n.line)
                    continue
                elif lines_number_btw_function_and_synch_block == 1:
                    # if there is any statement after SynchronizedStatement, then it's an anti-pattern
                    method_item = method_nodes[method_line]
                    if len(method_item.node.body) > 1 and \
                            isinstance(method_item.node.body[0], javalang.tree.SynchronizedStatement):
                        total_code_lines.add(sync_n.line)
                        continue

        return sorted(total_code_lines)
