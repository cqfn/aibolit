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
    def __work_with_stats(self, stats, flag_this, flag_else):
        for expr in stats:
            if isinstance(expr, javalang.tree.TryStatement):
                flag_try = 0
                if (expr.resources is not None) or (expr.catches[0].block != []) or (expr.finally_block is not None):
                    flag_try = 1
                try_exprs = expr.block
                for expr1 in try_exprs:
                    if isinstance(expr1, javalang.tree.StatementExpression):
                        if isinstance(expr1.expression, javalang.tree.ExplicitConstructorInvocation):
                            if flag_this + flag_else + flag_try != 0:
                                flag_this = 1
                                return 1, flag_this, flag_else
                            flag_this = 1
                        else:
                            if flag_this != 0:
                                return 1, flag_this, flag_else
                            flag_else = 1
                    else:
                        if flag_this != 0:
                            return 1, flag_this, flag_else
                        flag_else = 1
                flag_else = 1
            elif isinstance(expr, javalang.tree.StatementExpression):
                if isinstance(expr.expression, javalang.tree.ExplicitConstructorInvocation):
                    if flag_this + flag_else != 0:
                        flag_this = 1
                        return 1, flag_this, flag_else
                    flag_this = 1
                else:
                    if flag_this != 0:
                        return 1, flag_this, flag_else
                    flag_else = 1
            elif isinstance(expr, javalang.tree.IfStatement):
                result, flag_this, flag_else = self.__work_with_stats(expr.then_statement.statements, flag_this, flag_else)
                if flag_this == 1:
                    return 1, flag_this, flag_else
                if expr.else_statement is not None:
                    if isinstance(expr.else_statement, javalang.tree.IfStatement):
                        result, flag_this, flag_else = self.__work_with_stats(expr.else_statement.then_statement.statements, flag_this, flag_else)
                        if flag_this == 1:
                            return 1, flag_this, flag_else
                        if expr.else_statement.else_statement is not None:
                            result, flag_this, flag_else = self.__work_with_stats(expr.else_statement.else_statement.statements, flag_this, flag_else)
                            if flag_this == 1:
                                return 1, flag_this, flag_else
            elif isinstance(expr, javalang.tree.ForStatement):
                result, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else)
                if flag_this == 1:
                    return 1, flag_this, flag_else
            elif isinstance(expr, javalang.tree.WhileStatement):
                result, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else) 
                if flag_this == 1:
                    return 1, flag_this, flag_else
            elif isinstance(expr, javalang.tree.DoStatement):
                result, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else)
                if flag_this == 1:
                    return 1, flag_this, flag_else
            else:
                if flag_this != 0:
                    return 1, flag_this, flag_else
                flag_else = 1
        return 0, flag_this, flag_else
    def value(self, filename: str):
        tree = self.__file_to_ast(filename)
        num_str = []
        for path, node in tree.filter(javalang.tree.ConstructorDeclaration):
            number = node.position.line
            stats = node.children[-1]
            result, _, _ = self.__work_with_stats(stats, 0, 0)
            if result == 1:
                num_str.append(number)              
        return sorted(list(set(num_str)))