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


class ThisFinder:

    def __expr_stat(self, expr, flag_this, flag_else):
        '''function to work with StatementExpression block'''
        if isinstance(expr.expression, javalang.tree.ExplicitConstructorInvocation):
            if flag_this + flag_else > 0:
                return 1, flag_this, flag_else
            flag_this = 1
        else:
            if flag_this > 0:
                return 1, flag_this, flag_else
        flag_else = 1
        return 0, flag_this, flag_else

    def __try_stat(self, expr, flag_this, flag_else):
        '''function to work with TryStatement block'''
        if (expr.resources is not None) or \
            (expr.catches is not None and expr.catches[0].block != []) or \
                (expr.finally_block is not None):
            flag_else = 1
        try_exprs = expr.block
        for expr1 in try_exprs:
            if isinstance(expr1, javalang.tree.StatementExpression):
                res, flag_this, flag_else = self.__expr_stat(expr1, flag_this, flag_else)
                if res > 0:
                    return 1, flag_this, flag_else
            else:
                if flag_this > 0:
                    return 1, flag_this, flag_else
                flag_else = 1
        flag_else = 1
        return 0, flag_this, flag_else

    def __if_stat(self, expr, flag_this, flag_else):
        '''function to work with IfStatement block'''
        if expr.then_statement is not None:
            if hasattr(expr.then_statement, 'statements'):
                stmts = expr.then_statement.statements
            else:
                stmts = []
            res, flag_this, flag_else = self.__work_with_stats(stmts, flag_this, flag_else)
            if res > 0:
                return 1, flag_this, flag_else
        if expr.else_statement is not None:
            if isinstance(expr.else_statement, javalang.tree.IfStatement):
                res, flag_this, flag_else = self.__if_stat(expr.else_statement, flag_this, flag_else)
                if res > 0:
                    return 1, flag_this, flag_else
                return 0, flag_this, flag_else
            block = expr.else_statement
            res, flag_this, flag_else = self.__work_with_stats(block, flag_this, flag_else)
            if res > 0:
                return 1, flag_this, flag_else
        return 0, flag_this, flag_else

    # flake8: noqa
    def __work_with_stats(self, stats, flag_this, flag_else):
        '''function to work with objects in constructor'''
        for expr in stats:
            res = 0
            old_else = flag_else
            flag_else = 1
            if isinstance(expr, javalang.tree.TryStatement):
                res, flag_this, flag_else = self.__try_stat(expr, flag_this, old_else)
            elif isinstance(expr, javalang.tree.StatementExpression):
                res, flag_this, flag_else = self.__expr_stat(expr, flag_this, old_else)
            elif isinstance(expr, javalang.tree.IfStatement):
                res, flag_this, flag_else = self.__if_stat(expr, flag_this, flag_else)
            elif isinstance(expr, javalang.tree.ForStatement):
                if hasattr(expr.body, 'statements'):
                    res, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else)
            elif isinstance(expr, javalang.tree.WhileStatement):
                if hasattr(expr.body, 'statements'):
                    res, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else)
            elif isinstance(expr, javalang.tree.DoStatement):
                if hasattr(expr.body, 'statements'):
                    res, flag_this, flag_else = self.__work_with_stats(expr.body.statements, flag_this, flag_else)
            else:
                res = flag_this
            if res > 0:
                return 1, flag_this, flag_else
        return 0, flag_this, flag_else

    def value(self, filename: str):
        '''main function'''
        tree = AST(filename).value()
        num_str = []
        for path, node in tree.filter(javalang.tree.ConstructorDeclaration):
            number = node.position.line
            stats = node.children[-1]
            result, _, _ = self.__work_with_stats(stats, 0, 0)
            if result == 1:
                num_str.append(number)
        return sorted(list(set(num_str)))
