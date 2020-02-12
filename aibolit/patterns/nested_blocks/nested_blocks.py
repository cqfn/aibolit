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



class BlockType:
    FOR = javalang.tree.ForStatement      # FOR Block Statement
    IF = javalang.tree.IfStatement        # IF Block Statement


class NestedBlocks:
    def __init__(self, max_depth: int, block_type=BlockType.FOR):
        """
        Returns lines in the file where nested FOR/IF blocks are located
        :param max_depth:
        :param block_type:
        """
        self.max_depth = max_depth
        self.block_type = block_type

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return:
        """
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def __for_node_depth(self, tree: javalang.ast.Node, max_depth: int,
                         for_links: list = [], for_before: int = 0) -> None:
        """
        Takes AST tree and returns list of "FOR" AST nodes of depth greater
        or equal than max_depth
        :param tree:
        :param max_depth:
        :param for_links:
        :param for_before:
        :return:
        """
        if isinstance(tree, self.block_type):  # todo: add try-catch for TypeError
            for_before += 1
            if for_before >= max_depth:
                for_links.append(tree)

        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                self.__for_node_depth(node, max_depth, for_links, for_before)

    def __fold_traverse_tree(self, root: javalang.ast.Node, res: list) -> list:
        """
        Traverse AST tree and apply function to each node
        Accumulate results in the list and return
        :param root: 
        :param res: 
        :return: 
        """
        v = None if not hasattr(root, '_position') else root._position.line
        if v is not None:
            res.append(v)
        for child in root.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                self.__fold_traverse_tree(node, f)
        return res

    def value(self, filename: str) -> list:
        """
        Return line numbers in the file where patterns are found
        :param filename:
        :return:
        """
        tree = self.__file_to_ast(filename)
        for_links = []
        self.__for_node_depth(tree, max_depth=self.max_depth, for_links=for_links)
        n_lines = []

        for for_node in for_links:
            n_lines.append(min(self.__fold_traverse_tree(for_node, [])))

        return n_lines
