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
from enum import Enum


class NodeType(Enum):
    VAR = 1      # Variable Declaration
    METHOD = 2   # Method Declaration


class VarMiddle:
    '''
    Returns lines in the file where variables declared in the middle
    of the method
    '''

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def __check_var_declaration(self, pos: int, line_to_node_map, empty_lines: List[int]) -> bool:
        '''
        Check that VAR declaration line is near the method declaration
        Args:
            pos (int): Line number we are going to check.
            line_to_node_map (Map Int Node): Map line number to node object

        Returns:
            bool: True if VAR declaration is near method declaration
        '''

        if line_to_node_map.get(pos) != NodeType.VAR:
            raise ValueError('Variable declaration line is expected!')
        i = pos - 1
        while i > 0:
            if line_to_node_map.get(i) == NodeType.METHOD:
                return True
            if i in empty_lines:
                i -= 1
                continue
            if line_to_node_map.get(i) is None:
                return False
            i -= 1
        raise ValueError('Method declaration is not found')

    def __get_empty_lines(self, tree: javalang.tree.CompilationUnit) -> List[int]:
        '''Figure out lines that are either empty or multiline statements'''
        lines_with_nodes = [
            node.position.line for path, node in tree
            if hasattr(node, 'position') and node.position is not None
        ]
        max_line = max(lines_with_nodes)
        return set(range(1, max_line + 1)).difference(lines_with_nodes)

    def value(self, filename: str) -> List[int]:
        ''''''
        line_to_node_map = {}
        tree = self.__file_to_ast(filename)
        empty_lines = self.__get_empty_lines(tree)

        m_decls = tree.filter(javalang.tree.MethodDeclaration)
        v_decls = tree.filter(javalang.tree.LocalVariableDeclaration)
        m_poss = [(e.position.line, NodeType.METHOD) for _, e in m_decls]
        v_poss = [(e.position.line, NodeType.VAR) for _, e in v_decls]
        line_to_node_map = dict(m_poss + v_poss)

        return [
            line for line, _ in v_poss
            if not self.__check_var_declaration(line, line_to_node_map, empty_lines)
        ]
