from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from typing import List


class MultipleWhile:

    def __init__(self):
        pass

    def get_number_of_sequential_while_statement_in_function(self, tree: AST, node: int) -> int:
        list_while_nodes = []
        set_child_while_nodes = set()
        for child in tree.all_children_with_type(node, ASTNodeType.WHILE_STATEMENT):
            list_while_nodes.append(child)
            set_internal_while = set(tree.all_children_with_type(child, ASTNodeType.WHILE_STATEMENT))
            set_child_while_nodes = set.union(set_child_while_nodes, set_internal_while)
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
        for node in tree.nodes_by_type(ASTNodeType.METHOD_DECLARATION):
            if self.get_number_of_sequential_while_statement_in_function(tree, node) > 1:
                lines.append(tree.get_attr(node, 'source_code_line'))

        return lines
