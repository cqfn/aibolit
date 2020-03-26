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


class EmptyRethrow:

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
        tree = self.__file_to_ast(filename)
        total_code_lines = set()
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                for _, throw_node in try_node.filter(javalang.tree.ThrowStatement):
                    catch_classes = [x.parameter.name for x in try_node.catches]
                    mem_ref = throw_node.children[1]
                    if mem_ref.member in catch_classes:
                        total_code_lines.add(mem_ref.position.line)

        return sorted(total_code_lines)
