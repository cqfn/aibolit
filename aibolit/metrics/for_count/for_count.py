import javalang
import click
from typing import List


class ForLoopNumber:
    '''
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

    def value(self, filename: str):
        tree = self.__file_to_ast(filename)
        for_links = []
        self.__for_node_depth(
            tree,
            for_max_depth=self.for_max_depth,
            for_links=for_links
        )
        return len(for_links)


@click.command()
@click.argument('filename')
@click.option('--for_max_depth', '-md', default=2)
def main(filename: str, for_max_depth: int = 2):
    for_loop_n_metric = ForLoopNumber(for_max_depth)
    n = for_loop_n_metric.value(filename)
    print(n)


if __name__ == "__main__":
    main()
