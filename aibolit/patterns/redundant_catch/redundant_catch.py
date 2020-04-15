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

import itertools
from collections import defaultdict
from collections import namedtuple

import javalang

from aibolit.patterns.var_middle.var_middle import JavalangImproved

ExceptionInfo = namedtuple('ExceptionInfo', 'func_name, catch_list, throws_list, line_number')


class RedundantCatch:
    """
    Find pattern when a method in Java class throws an exception,
    and the exception of the same type is caught inside the method.

    E.g.,
    class Book {
    void foo() throws IOException {
        try {
          Files.readAllBytes();
        } catch (IOException e)
          { // here
          // do something
          }
        }
    }
    Here, the method foo() throws IOException, but we catch it inside the method
    """
    def __init__(self):
        pass

    def value(self, filename):
        """
        Find the mentioned-above pattern
        :param filename: filename of Java file
        :return: code lines of try statement where it was found
        """
        total_code_lines = set()
        obj = JavalangImproved(filename)
        items = obj.tree_to_nodes()
        try_nodes = defaultdict(list)
        method_nodes = {}
        for x in items:
            # Line break occurred before a binary operator (W503)
            # But this rule goes against the PEP 8 recommended style, so
            # replace isinstanceof with variable
            is_instance_meth_decl = isinstance(x.node, javalang.tree.MethodDeclaration)
            is_instance_try_stat = isinstance(x.node, javalang.tree.TryStatement)
            is_instance_ctor_decl = isinstance(x.node, javalang.tree.ConstructorDeclaration)
            is_instance_lambda = isinstance(x.node, javalang.tree.LambdaExpression)
            if is_instance_try_stat and x.method_line and not is_instance_lambda:
                # If we do not have a line for method, we ignore this method
                try_nodes[x.method_line].append(x)
            elif (is_instance_meth_decl or is_instance_ctor_decl) and x.method_line and not is_instance_lambda:
                # If we do not have a line for method, we ignore this method
                method_nodes[x.method_line] = x

        for method_line, iter_nodes in sorted(try_nodes.items(), key=lambda x: x[1][0].line):
            for try_node in iter_nodes:
                method_node = method_nodes.get(method_line)

                if not method_node or not method_node.node.throws:
                    continue

                catch_list = []
                ei = ExceptionInfo(
                    func_name=method_node.node.name,
                    catch_list=catch_list,
                    throws_list=method_node.node.throws,
                    line_number=method_node.node.position.line
                )
                if try_node.node.catches:
                    catch_classes = [x.parameter.types for x in try_node.node.catches]
                    classes_exception_list = list(itertools.chain(*catch_classes))
                    ei.catch_list.extend(classes_exception_list)

                    lines_number = set([
                        try_node.line for c in ei.catch_list if c in ei.throws_list
                    ])
                    total_code_lines.update(lines_number)

        return sorted(total_code_lines)
