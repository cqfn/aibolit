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


# mapping between javalang node class names and Java keywords
NODE_KEYWORD_MAP = {
    'SuperMethodInvocation': 'super',
    'WhileStatement': 'while',
    'ForStatement': 'for',
    'TryStatement': 'try',
    'CatchClause': 'catch',
}


class ASTNode:
    def __init__(self, line, method_line, node):
        self.line = line  # node line number in the file
        self.method_line = method_line  # line number where parent method declared
        self.node = node  # javalang AST node object


class JavalangImproved:

    def __init__(self, filename: str):
        tree, lines = self.__file_to_ast(filename)
        self.tree = tree
        self.lines = lines

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())
            lines = file.readlines()

        with open(filename, encoding='utf-8') as file:
            lines = file.readlines()

        return tree, lines

    def __find_keyword(self, lines, keyword, start):
        for i in range(start - 1, len(lines)):
            if keyword in lines[i]:
                return i + 1
        return -1

    def __fix_line_number_if_possible(self, node: javalang.ast.Node, line_n):
        node_class_name = node.__class__.__name__
        if node_class_name not in NODE_KEYWORD_MAP:
            return line_n
        line = self.__find_keyword(
            self.lines,
            NODE_KEYWORD_MAP[node_class_name],
            line_n
        )
        if line == -1:
            return line_n
        return line

    def __tree_to_nodes(self, tree: javalang.ast.Node, line=1, parent_method_line=None) -> List[ASTNode]:
        '''Return AST nodes with line numbers sorted by line number'''

        if hasattr(tree, 'position') and tree.position:
            line = tree.position.line

        line = self.__fix_line_number_if_possible(tree, line)
        if type(tree) == javalang.tree.MethodDeclaration:
            parent_method_line = line
        res = []
        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                left_siblings_line = res[-1].line if len(res) > 0 else line
                res += self.__tree_to_nodes(
                    node,
                    left_siblings_line,
                    parent_method_line
                )

        return [ASTNode(line, parent_method_line, tree)] + res

    def tree_to_nodes(self) -> List[ASTNode]:
        '''Return AST nodes as list with line numbers sorted by line number'''
        nodes = self.__tree_to_nodes(self.tree)
        return sorted(nodes, key=lambda v: v.line)

    def filter(self, ntypes: [javalang.tree.Node]) -> List[ASTNode]:
        nodes = self.tree_to_nodes()
        return list(
            filter(lambda v: type(v.node) in ntypes, nodes)
        )

    def get_empty_lines(self) -> List[int]:
        '''Figure out lines that are either empty or multiline statements'''
        lines_with_nodes = list(map(lambda v: v.line, self.tree_to_nodes()))
        # lines_with_nodes = [
        #     node.position.line for path, node in self.tree
        #     if hasattr(node, 'position') and node.position is not None
        # ]
        max_line = max(lines_with_nodes)
        return set(range(1, max_line + 1)).difference(lines_with_nodes)


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

    def __check_var_declaration(self, pos: int, line_to_node_map, empty_lines: List[int]) -> bool:
        '''
        Check that VAR declaration line is near the method declaration
        Args:
            pos (int): Line number we are going to check.
            line_to_node_map (Map Int Node): Map line number to node object

        Returns:
            bool: True if VAR declaration is near method declaration
        '''
        ntype, method = line_to_node_map.get(pos)
        if ntype != NodeType.VAR:
            raise ValueError('Variable declaration line is expected!')
        i = pos - 1
        while i > 0:
            if i in empty_lines:
                i -= 1
                continue
            if i not in line_to_node_map:
                return False

            _ntype, _method = line_to_node_map.get(i)
            if _ntype == NodeType.METHOD and method == _method:
                return True
            if _ntype == NodeType.VAR and method != _method:
                return False

            i -= 1
        raise ValueError('Method declaration is not found')

    def __get_other_statements_with_vars_declarations(self, nodes):
        ntypes = [javalang.tree.TryResource]
        return list(
            filter(lambda v: v['ntype'] in ntypes, nodes)
        )

    def value(self, filename: str) -> List[int]:
        ''''''
        line_to_node_map = {}

        tree = JavalangImproved(filename)
        empty_lines = tree.get_empty_lines()
        m_decls = tree.filter([javalang.tree.MethodDeclaration])
        v_decls = tree.filter([
            javalang.tree.LocalVariableDeclaration,
            javalang.tree.TryResource
        ])

        m_poss = [(e.line, (NodeType.METHOD, e.method_line)) for e in m_decls]
        v_poss = [(e.line, (NodeType.VAR, e.method_line)) for e in v_decls]
        line_to_node_map = dict(m_poss + v_poss)

        return [
            line for line, _ in v_poss
            if not self.__check_var_declaration(line, line_to_node_map, empty_lines)
        ]
