import javalang
import click
from typing import List, Callable, Optional, Any


class ForNested:
    '''
    Returns lines in the file where 
    Count number of FOR loops
    '''

    def __init__(self, for_max_depth: int):
        self.for_max_depth = for_max_depth

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename) as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def __for_node_depth(
        self,
        tree: javalang.ast.Node,
        for_max_depth: int,
        for_links: List = [],
        for_before: int = 0
    ) -> None:
        '''
        Takes AST tree and returns list of "FOR" AST nodes of depth greater
        or equal than for_max_depth
        '''
        if (type(tree) == javalang.tree.ForStatement):
            for_before += 1
            if for_before >= for_max_depth:
                for_links += [tree]

        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                self.__for_node_depth(node, for_max_depth, for_links, for_before)

    def __fold_traverse_tree(
        self,
        root: javalang.ast.Node,
        f: Callable[[javalang.ast.Node], Optional[Any]]
    ) -> [Any]:
        ''' 
        Traverse AST tree and apply function to each node
        Accumulate results in the list and return
        '''
        res = []
        v = f(root)
        if v is not None:
            res.append(v)

        for child in root.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                res += self.__fold_traverse_tree(node, f)

        return res


    def value(self, filename: str) -> [int]:
        '''Return line numbers in the file where patterns are found'''
        tree = self.__file_to_ast(filename)
        for_links = []
        self.__for_node_depth(
            tree,
            for_max_depth=self.for_max_depth,
            for_links=for_links
        )

        def find_line_position(node: javalang.ast.Node) -> int:
            if hasattr(node, '_position'):
                return node._position.line
            else:
                None

        n_lines = [
            self.__fold_traverse_tree(for_node, find_line_position) 
            for for_node in for_links
        ]

        return list(map(min, n_lines))

