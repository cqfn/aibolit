from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from typing import List, Set


class MultipleWhile:

    def __init__(self):
        pass

    def get_top_level_while_qty(self, tree: AST, node: int) -> int:
        list_while_nodes: List[int] = []
        set_child_while_nodes: Set[int] = set()
        for child in tree.all_children_with_type(node, ASTNodeType.WHILE_STATEMENT):
            list_while_nodes.append(child)
            set_internal_while = set(tree.list_all_children_with_type(child, ASTNodeType.WHILE_STATEMENT))
            set_child_while_nodes |= set_internal_while
        return len(list_while_nodes) - len(set_child_while_nodes)

    def value(self, filename: str) -> List[int]:
        """
        Travers over AST tree and finds function with sequential while statement
        :param filename:
        :return:
        List of LineNumber of methods which have sequential while statements
        """

        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for node in tree.get_nodes(ASTNodeType.METHOD_DECLARATION):
            if self.get_top_level_while_qty(tree, node) > 1:
                lines.append(tree.get_attr(node, 'line'))

        return lines
