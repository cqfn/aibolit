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
    # flake8: noqa: C901
    def value(self, filename: str):
        tree = self.__file_to_ast(filename)
        num_str = []
        for path, node in tree.filter(javalang.tree.ConstructorDeclaration):
            number = node.position.line
            stats = node.children[-1]
            flag_super = 0
            flag_this = 0
            flag_else = 0
            for expr1 in stats:
                expr = expr1
                if isinstance(expr, javalang.tree.TryStatement):
                    if (expr.resources is not None) or (expr.catches[0].block != []) or (expr.finally_block != []):
                        num_str.append(number)
                        break
                    expr = expr1.block
                if isinstance(expr, javalang.tree.StatementExpression):
                    if isinstance(expr.expression, javalang.tree.SuperConstructorInvocation):
                        if flag_this + flag_else != 0:
                            num_str.append(number)
                            break
                        flag_super = 1
                    elif isinstance(expr.expression, javalang.tree.ExplicitConstructorInvocation):
                        if flag_this + flag_else != 0:
                            num_str.append(number)
                            break
                        flag_this = 1
                    else:
                        if flag_this + flag_super != 0:
                            num_str.append(number)
                            break
                        flag_else = 1
                else:
                    if flag_this + flag_super != 0:
                            num_str.append(number)
                            break
                    flag_else = 1
            
        return sorted(list(set(num_str)))
