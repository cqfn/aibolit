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
from typing import List


class VarDeclarationDistance:
    '''
    Returns lines where variable first time used but declared more than
    specific number of lined before
    '''

    def __init__(self, lines_th: int):
        self.__lines_th = lines_th

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

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

    def __tree_to_list(self, tree: javalang.tree.CompilationUnit) -> List[object]:
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

    def __get_empty_lines(self, tree: javalang.tree.CompilationUnit) -> List[int]:
        '''Figure out lines that are either empty or multiline statements'''
        lines_with_nodes = [
            node.position.line for path, node in tree
            if hasattr(node, 'position') and node.position is not None
        ]
        max_line = max(lines_with_nodes)
        return set(range(1, max_line + 1)).difference(lines_with_nodes)

    def __group_vars_by_method(self, items: List[object]) -> List[object]:
        '''
        Group variables by method scope and calculate for each the declaration
        line and first usage line
        '''
        var_scopes = []
        vars = {}
        for item in items:
            if item['ntype'] in [javalang.tree.MethodDeclaration]:
                vars = {}
                var_scopes += [vars]
                continue

            if (item['ntype'] == javalang.tree.VariableDeclarator):
                vars[item['name']] = {'decl': item['line'], 'first_usage': None}
                continue

            if (item['ntype'] == javalang.tree.VariableDeclarator):
                vars[item['name']] = {'decl': item['line']}
                continue

            if item['name'] in vars.keys() and vars[item['name']]['first_usage'] is None:
                vars[item['name']]['first_usage'] = item['line']

        return var_scopes

    def __line_diff(self, usage_line: int, declaration_line: int, empty_lines: List[int]) -> int:
        '''
        Calculate line difference between variable declaration and first usage
        taking into account empty lines
        '''
        lines_range = set(range(declaration_line + 1, usage_line))
        return len(lines_range.difference(empty_lines))

    def value(self, filename: str) -> List[int]:
        ''''''

        tree = self.__file_to_ast(filename)
        items = self.__tree_to_list(tree)
        var_scopes = self.__group_vars_by_method(items)
        empty_lines = self.__get_empty_lines(tree)

        violations = []
        for scope in var_scopes:
            for var in scope:
                if scope[var]['first_usage'] is None:
                    continue

                line_diff = self.__line_diff(
                    scope[var]['first_usage'],
                    scope[var]['decl'],
                    empty_lines
                )
                if line_diff < self.__lines_th:
                    continue

                violations.append(scope[var]['first_usage'])

        return violations
